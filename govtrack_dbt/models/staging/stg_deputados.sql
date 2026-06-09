SELECT id, nome, "siglaPartido", "siglaUf", "idLegislatura", email
FROM {{ ref('deputados') }}
WHERE nome IS NOT NULL