## Cliente

**Descrição**: Este código permite que um cliente se conecte a um servidor de chat, envie mensagens para o servidor e receba mensagens do servidor de forma assíncrona, enquanto também aceita entrada do usuário em uma thread separada.

### Principais características:

* É definida uma função `user_input_thread` que será executada em uma thread separada para lidar com a entrada do usuário. Essa função lê a entrada do usuário e envia as mensagens para o servidor.

* O código lida com o endereço IP e porta. Uma conexão de soquete é criada usando o endereço IP e porta fornecidos, e o cliente se conecta ao servidor.

* Uma thread separada chamada user_input_thread é iniciada para lidar com a entrada do usuário de forma assíncrona. Esta thread permite que o cliente aceite entrada do usuário enquanto aguarda mensagens do servidor.

* Se o cliente enviar a mensagem "@SAIR", o cliente será desconectado e o programa será encerrado.

## Servidor

**Descrição**: Esse código implementa um servidor de chat básico que aceita múltiplas conexões de clientes e permite que eles conversem entre si, além de ordenar as mensagens e realizar o rastreamento de nomes de usuário.

### Principais características

* A função `chat_client` é definida para lidar com a comunicação com um cliente específico. Ela recebe uma conexão conn e um endereço como argumentos.

* O código lê o nome de usuário enviado pelo cliente através da conexão. Se o nome de usuário estiver vazio ou já estiver em uso, o cliente é notificado e a conexão é encerrada. Caso contrário, o nome de usuário é registrado no dicionário usernames.

* O código entra em um loop onde aguarda mensagens do cliente. Ele verifica se o cliente deseja sair, ordenar as mensagens ou enviar uma mensagem regular. As mensagens são processadas e distribuídas para outros clientes conectados.

* A função `store_message` é responsável por armazenar mensagens no servidor, juntamente com uma marcação de data/hora. Ela também controla o tamanho máximo da lista de mensagens, excluindo as mais antigas se necessário.

* A função `send_ordered_messages` envia as mensagens armazenadas no servidor para o cliente que fez a solicitação de ordenação. As mensagens são ordenadas por data/hora antes de serem enviadas.

* Além disso, o código define as configurações de um servidor socket, ligado a todas as interfaces de rede (0.0.0.0) e colocado em estado de escuta para aceitar conexões de clientes.