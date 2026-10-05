SELECT codigoEmenda, autor,valorPago, funcao, localidadeDoGasto FROM {{ ref('stg_emendas') }}
