# [ATUALIZAÇÕES:](./UPDATES.md#vers%C3%A3o-10---31072024)

## VERSÃO 1.3 - 09/06/2025:
* ✅Arquivos ocultos e de sistema são ignorados automaticamente durante o processo de conversão — mesmo que estejam visíveis no Explorador do Windows.
---

## VERSÃO 1.2 - 24/05/2025:
* ✅Adicionada barra de progresso e melhorias no status, que agora exibe o diretório, progresso e pasta final da conversão.
* ✅Agora o usuário seleciona uma pasta em vez de arquivos individuais, e as imagens convertidas são salvas automaticamente em uma subpasta `CONVERTIDOS_<FORMATO>`.
* ✅O botão "SALVAR" foi renomeado para "CONVERTER".
* ✅Os botões "DIRETÓRIO" e "CONVERTER" agora estão lado a lado.
* ✅Adicionados um campo de status e uma barra de progresso para exibir o diretório selecionado e o andamento da conversão em tempo real.
* ✅A interface inicia com zoom total e suporte a rolagem vertical.
* ✅O layout foi reorganizado, com os campos "CONVERTER PARA" e "REMOVER FUNDO" em containers próprios, e o `footer` foi removido.
---

## VERSÃO 1.1 - 20/05/2025:
* ✅O aplicativo agora se chama "IMAGEM CONVERTER";
* ✅Migrado para `CustomTkinter`, com botões de rádio lado a lado e feedback ao usuário feito apenas por pop-ups.
* ✅Os aplicativos apagados foram: "IMAGEM PARA ICO" (21/03/2024) e "REMOVEDOR DE FUNDO DE IMAGEM" (14/03/2024).
---

## VERSÃO 1.0 - 31/07/2024:
**✅Aplicativo lançado oficialmente com o nome `IMAGEM PARA CONVERSAO`, desenvolvido com `Tkinter`:**
- 🔹A interface conta com o botão `SELECIONAR` para escolher o diretório, e logo abaixo é exibido um `Label` mostrando o caminho selecionado.  
- 🔹Em seguida, há os botões de opção (radio buttons) para selecionar o formato de conversão em **"CONVERTER PARA:"**, com as opções: `PADRÃO`, `ICO`, `PNG`, `JPG` e `JPEG`.  
- 🔹Abaixo disso, há também radio buttons com as opções `SIM` e `NÃO` para que o usuário decida se deseja remover o fundo da imagem selecionada (função realizada com a biblioteca `rembg`).  
- 🔹Logo abaixo, há o botão `SALVAR`, que ao ser clicado salva a imagem convertida no mesmo diretório, com o nome no formato: `{NOME}_IMAGEM_CONVERTIDA_{FORMATO}`.
- 🔹Por fim, a seção de `footer` foi adicionada, exibindo o nome do criador e o username do GitHub.


