SELECT 
    id,
    nome,
    siglaPartido as siglapartido,
    siglaUf as siglauf,
    idLegislatura as idlegislatura,
    email
FROM {{ source('govtrack_bruto', 'deputados_bruto') }}
WHERE nome IS NOT NULL