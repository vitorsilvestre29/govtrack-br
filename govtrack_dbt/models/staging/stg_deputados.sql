SELECT id, nome, siglapartido, siglauf, idlegislatura, email 
FROM {{ ref('deputados') }}
WHERE nome IS NOT NULL