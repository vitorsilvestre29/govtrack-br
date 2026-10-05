SELECT 
    codigoEmenda, ano, tipoEmenda, autor, localidadeDoGasto, funcao, valorPago
FROM {{ source('govtrack_bruto', 'emendas_bruto') }}