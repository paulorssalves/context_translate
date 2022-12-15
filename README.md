# context_translate
	
Um script para, de uma lista .csv, pegar palavras e frases em contexto e suas respectivas traduções e enviar para outra lista .csv. 

## Dependências

- pandas
- [Reverso Context API](https://github.com/flagist0/reverso_context_api)

## Exemplos

### Como iniciar o programa

O programa toma como padrão a presença de um arquivo de input denominado `words.csv` na mesma pasta em que ele se encontra. Todavia, este pode ser substituído por um outro arquivo .csv da sua escolha. Exemplos:

>python translate.py

Válido. Toma `words.csv` como input.

>python translate.py palavras.csv

Válido. Toma `palavras.csv` como input

>python translate.py palavras.csv termos.csv

Inválido. Até o presente momento o programa só pode interagir com um arquivo .csv de cada vez.

### Exemplo de input-output

Input:

| Palavras-base |
|---|
| предложение |
| достаточно|
| трудно|

Output:

| Palavras-base | Tradução | Frase de exemplo | Tradução da frase |
|---|----|----|----|
| предложение | proposal<br><br>offer<br><br>sentence | Можешь выставлять своё предложение на голосование.<br><br>Спонтанное предложение Кита начнется через минуту.<br><br>Они не отклонят предложение из-за одной неудачи. | You go right ahead and put your proposal to a vote.<br><br>Keith's spontanoeus proposal to Elliot will be happening in exactly one minute.<br><br>They're not going to withdraw the offer because you had a setback.
| достаточно| enough<br><br>sufficiently<br><br>fairly |Абсолютно, я достаточно домов построил.<br><br>Часть о нежелании умирать достаточно правдива.<br><br>Конечно, если ты достаточно отдохнула.| Hell, yes. I've built enough homes to know that.<br><br>The part about not wanting to die... that's true enough.<br><br>I mean, if you're sufficiently rested, of course.|
| трудно*| difficult<br><br>hard<br><br>easily|Но это трудно и требует здравомыслия.<br><br>Мне сейчас трудно находиться среди незнакомых людей.<br><br>Иногда это трудно и невозможно понять.|But it's difficult, and we need to be conscious.<br><br>I kind of have a hard time around people I don't know.<br><br>Sometimes it's just difficult, you know, and you can't.|


\* "Трудно" **não** é equivalente a "easily". Esse output ocorre porque essa palavra é comumente traduzida como "not easily", e o Context Reverso entrega as coisas dessa forma.

## Adendos

Não altere o intervalo entre requests feitas ao servidor. Há um intervalo de 5 segundos + um time.sleep() aleatório de duração < 1 segundo. O propósito disso é manter o comportamento do padrão dentro das exigências do servidor. Diminuir o intervalo pode resultar em banimento do site, o que inutiliza o programa.

## Línguas disponíveis

Russo e inglês **não** são as únicas línguas disponíveis. Basta trocar as configurações para a língua desejada, desde que a opção desta língua exista no Context Reverso. Basta ir em `tools.py` e trocar para as línguas desejadas o par de variáveis em `LANGUAGE_TUPLE`. O primeiro item é a SOURCE LANGUAGE, ou a língua _de que_ se traduz, e o segundo item é a TARGET LANGUAGE, ou a língua _para qual_ se traduz.

## Afazeres

  - Exception Handling -- Duas alternativas:
      1. Usar threading. Se uma resposta demorar demais, de alguma forma cancelar o pedido e ir para a próxima, ou pedir apenas um exemplo.
  - Enxugar código:
    - Adicionar opções de línguas de forma explícita, de acordo com os idiomas disponíveis no Context Reverso
    	- Incluir tais opções no prompt
  - ~inserir dados do wiktionary se eles existirem, quando `word_data = False` em `translate.py`~
  - verificar a possibilidade de procurar exemplos de frases *mesmo se* não houver traduções objetivas. Para isso é necessário verificar a funcionalidade das exception handlings do primeiro ponto desta lista. 


