SELECT siglapartido, COUNT(*) AS total_deputados 
FROM {{ ref('stg_deputados') }}
GROUP BY siglapartido
ORDER BY total_deputados DESC