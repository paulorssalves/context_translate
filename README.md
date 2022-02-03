# context_translate
	
Um script para, de uma lista .csv, pegar palavras e frases em contexto e suas respectivas traduções e enviar para outra lista .csv. 


## Exemplo

Input:

| palavras iniciais |
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

## Adendos

Palavras que não têm ao menos uma opção de tradução no Reverso Context serão procuradas no Wiktionary e colocadas junto de suas definições em uma arquivo .csv alternativo. A cada 20 palavras, haverá um intervalo de 30 segundos para evitar que os servidores bloqueiem o IP do usuário por excesso de requests. Os exemplos são do russo para o inglês pois (1) no momento em que estou desenvolvendo este programa estou no processo de aprender russo e (2) pois inglês é a língua com maior número de resultados no dicionário utilizado. 

## Línguas disponíveis

Russo e inglês **não** são as únicas línguas disponíveis. Basta trocar as configurações para a língua desejada, desde que a opção desta língua exista no Context Reverso. Basta ir em `tools.py` *e* em `words.py` e trocar para as línguas desejadas as variáveis `INPUT_LANGUAG` e `OUTPUT_LANGUAGE`. 

---

- **TODO**:
  - Exception Handling -- Duas alternativas:
      1. Quando houver uma palavra que não tem pelo menos três exemplos, pegar o HTTPError e pedir por apenas um exemplo
      2. Usar threading. Se uma resposta demorar demais, de alguma forma cancelar o pedido e ir para a próxima, ou pedir apenas um exemplo.
  - Enxugar código:
    - Adicionar opções de línguas de acordo com os idiomas disponíveis no Context Reverso
    	- Incluir tais opções no prompt
  - inserir dados do wiktionary se eles existirem, quando word_data = False em `translate.py`
  - verificar a possibilidade de procurar exemplos de frases *mesmo se* não houver traduções objetivas. Para isso é necessário verificar alguns 

----


\* "Трудно" **não** é equivalente a "easily". Esse output ocorre porque essa palavra é comumente traduzida como "not easily", e o Context Reverso entrega as coisas dessa forma.