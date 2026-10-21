# PhysAI

IA interpretável para eventos extremos.

PhysAI é uma biblioteca e conjunto de benchmarks para estudar explicabilidade em séries temporais com eventos extremos. O núcleo inicial do projeto é um cenário sintético com verdade conhecida, em que um driver físico gera uma resposta com defasagem, ruído e limiar de evento extremo.

- Site: https://example.com/physai
- Documentação: https://physai.readthedocs.io
- Código: https://github.com/helioai/physai

## Visão
A ideia central é combinar dinâmica física, séries temporais e explicabilidade para avaliar se uma explicação aponta a causa verdadeira e não apenas um padrão correlacionado.

## Instalação

```bash
py -m pip install -e .
```

## Uso rápido

Benchmark de um cenário:

```bash
py -m pacote.cli.commands run --scenario driver_response --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --seed 0 --epochs 5 --output-dir runs/demo
```

Benchmark multi-cenário:

```bash
py -m pacote.cli.commands suite --scenarios driver_response,pulse_response --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --seed 0 --epochs 5 --output-dir runs/suite
```

Para comandos individuais:

```bash
py -m pacote.cli.commands synth --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --seed 0
py -m pacote.cli.commands train --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --epochs 5
py -m pacote.cli.commands explain --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05 --window-size 5
py -m pacote.cli.commands eval --n-samples 256 --lag 4 --coupling 1.3 --noise 0.05
```

## Estrutura
- Dados: fontes e carregadores
- Modelos: baselines e redes neurais
- Explicabilidade: SHAP, oclusão e interpretação
- Relatórios: resultados reprodutíveis e documentação

## Milestone atual
O v0.1 do projeto está focado em um benchmark sintético com verdade conhecida, avaliação sem vazamento temporal e métricas de fidelidade da explicação.
