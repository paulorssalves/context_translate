# context_translate
	
Um script para, de uma lista .csv, pegar palavras e frases em contexto e suas respectivas traduções e enviar para outra lista .csv. 

Input:

| palavras iniciais |
|---|
| предложение |
| достаточно|
| трудно|
| добрый |

Output:

| palavras iniciais | tradução | frase | tradução da frase |
|---|----|----|----|
| предложение | suggestion | três exemplos em russo | três exemplos em inglês |*
| достаточно| enough\*\* |três exemplos em russo | três exemplos em inglês |
| трудно| difficult |três exemplos em russo | três exemplos em inglês |
| добрый | good |três exemplos em russo | três exemplos em inglês |

----

Palavras que não têm ao menos uma opção de tradução no Reverso Context serão procuradas no Wiktionary e colocadas junto de suas definições em uma arquivo .csv alternativo. A cada 20 palavras, haverá um intervalo de 30 segundos para evitar que os servidores bloqueiem o IP do usuário por excesso de requests. 

- **TODO**:
  - Exception Handling -- Duas alternativas:
      1. Quando houver uma palavra que não tem pelo menos três exemplos, pegar o HTTPError e pedir por apenas um exemplo
      2. Usar threading. Se uma resposta demorar demais, de alguma forma cancelar o pedido e ir para a próxima, ou pedir apenas um exemplo.
  - Enxugar código:
    - Pegar as partes que fazem requests para os sites e transformá-las em funções
    - Executar processo central dentro de um `if __name__ == "__main__"` 

----

- *Importante: russo e inglês são simplesmente o que está configurado. Qualquer outra língua selecionável no reverso context funciona, só tem que editar o código fonte.

- \*\* cinco exemplos, se disponíveis 




