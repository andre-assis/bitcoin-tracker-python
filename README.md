# Monitoramento do Preço do Bitcoin com Alerta por Email

## Descrição
Este projeto é uma solução de RPA (Automação de Processos Robóticos) que monitora o preço do Bitcoin em tempo real e envia um alerta por email caso o valor fique abaixo de um limite definido. O preço é obtido através da API da CoinGecko, e a verificação ocorre a cada 30 minutos.

## Funcionalidades
- Consumo da API do CoinGecko para obter o preço atual do Bitcoin em Reais (BRL).
- Comparação automática do preço atual com um limite predefinido.
- Envio de email de alerta caso o preço fique abaixo do limite estipulado.
- Agendamento de verificações automáticas a cada 30 minutos.