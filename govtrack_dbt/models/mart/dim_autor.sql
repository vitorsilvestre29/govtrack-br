SELECT DISTINCT autor,
  CASE WHEN autor LIKE '%FINANCAS E TRIBUTACAO%' THEN 'Comissão de Finanças e Tributação'
       WHEN autor LIKE '%COM%' THEN 'Comissão'
       WHEN autor LIKE '%BANCADA%' THEN 'Bancada'
       WHEN autor LIKE '%RELATOR%' THEN 'Relator'
       WHEN autor = 'Sem informação' THEN 'Sem informação'
       ELSE 'Outro'
  END AS tipo_autor
FROM {{ ref('stg_emendas') }}