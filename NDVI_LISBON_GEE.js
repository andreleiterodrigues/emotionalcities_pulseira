// Define o shapefile da área de interesse (AOI)
var aoi = ee.FeatureCollection("projects/ee-andreleiterodrigues/assets/Limite_lisbon");
var aoiGeometry = aoi.geometry(); // Garante o uso da área completa como única geometria

// Define o intervalo de meses para análise
var meses = ['2024-08', '2024-09', '2024-10', '2024-11', '2024-12'];

// Função para aplicar máscara de nuvens usando MSK_CLDPRB
function mascararNuvens(image) {
  var cloudMask = image.select('MSK_CLDPRB').lte(10); // Mantém pixels com menos de 10% de probabilidade de nuvem
  return image.updateMask(cloudMask);
}

// Função para calcular o NDVI
function calcularNDVI(image) {
  return image.normalizedDifference(['B8', 'B4']).rename('NDVI');
}

// Função para filtrar e processar imagens com menor cobertura de nuvens
function filtrarMelhorImagem(mes) {
  var inicio = ee.Date(mes + '-01');
  var fim = inicio.advance(1, 'month');

  // Filtrar a coleção Sentinel-2
  var colecao = ee.ImageCollection('COPERNICUS/S2_SR') // Usando a coleção Surface Reflectance
    .filterBounds(aoiGeometry)
    .filterDate(inicio, fim)
    .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', 50)) // Filtra imagens com até 50% de nuvens
    .map(mascararNuvens); // Aplica a máscara de nuvens

  // Criar mosaico se necessário (usar a média das imagens disponíveis)
  var melhorImagem = colecao.median();

  // Calcular o NDVI
  var ndvi = calcularNDVI(melhorImagem).clip(aoiGeometry);

  return ndvi.set('mes', mes); // Adiciona o atributo do mês
}

// Loop para processar cada mês
var resultadosNDVI = meses.map(function(mes) {
  return filtrarMelhorImagem(mes);
});

// Visualizar NDVI no mapa
resultadosNDVI.forEach(function(ndvi, indice) {
  var imagemNDVI = ee.Image(ndvi);
  var nomeCamada = 'NDVI ' + meses[indice];
  Map.addLayer(imagemNDVI, {min: 0, max: 1, palette: ['blue', 'white', 'green']}, nomeCamada);
});

// Exportar cada NDVI como GeoTIFF
resultadosNDVI.forEach(function(ndvi, indice) {
  var nomeArquivo = 'NDVI_' + meses[indice].replace('-', '_');
  Export.image.toDrive({
    image: ee.Image(ndvi),
    description: nomeArquivo,
    folder: 'GEE_Exports',
    fileNamePrefix: nomeArquivo,
    region: aoiGeometry,
    scale: 10,
    crs: 'EPSG:4326', // Projeção WGS84
    maxPixels: 1e13
  });
});

print('Processamento concluído. Verifique o mapa para pré-visualizar os NDVI e use o painel Tasks para exportação.');
