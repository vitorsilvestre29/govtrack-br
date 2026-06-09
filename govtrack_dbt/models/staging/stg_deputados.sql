SELECT 
    id,
    nome,
    "siglaPartido" as siglapartido,
    "siglaUf" as siglauf,
    "idLegislatura" as idlegislatura,
    email
FROM {{ ref('deputados') }}
WHERE nome IS NOT NULL