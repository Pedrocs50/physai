# Primeiros passos

Este guia documenta a primeira etapa do projeto: o benchmark sintético do v0.1.

## Objetivo
Validar um fluxo mínimo de:

1. geração do cenário sintético,
2. treino de um modelo simples,
3. explicação por oclusão,
4. avaliação de fidelidade,
5. geração de relatório reprodutível.

## Instalação

```bash
py -m pip install -e .
```

## Fluxo mínimo

```bash
py -m pacote.cli.commands synth --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --seed 0
py -m pacote.cli.commands train --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --epochs 5
py -m pacote.cli.commands explain --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --window-size 5
py -m pacote.cli.commands eval --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05
py -m pacote.cli.commands report --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05
```

Ou, em uma execução completa do benchmark por cenário:

```bash
py -m pacote.cli.commands run --scenario driver_response --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --seed 0 --epochs 5 --output-dir runs/demo
```

Para comparar cenários em uma mesma suíte:

```bash
py -m pacote.cli.commands suite --scenarios driver_response,pulse_response --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --seed 0 --epochs 5 --output-dir runs/suite
```

## O que está sendo validado
- geração do driver e da resposta
- máscara causal e evento extremo
- treino não supervisonado da sequência reduzida
- explicação por remoção local
- métricas de fidelidade da explicação

## Próximo passo
A próxima etapa do projeto é ampliar esse núcleo para múltiplos cenários sintéticos, métricas adicionais e a camada de CLI mais rica. O benchmark em suíte já está disponível como evolução direta do v0.1, permitindo comparar diferentes famílias de cenários dentro do mesmo fluxo reprodutível.
