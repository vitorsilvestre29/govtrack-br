SELECT "siglaPartido", COUNT(*) AS total_deputados 
FROM {{ ref('stg_deputados') }}
GROUP BY "siglaPartido"
ORDER BY total_deputados DESC