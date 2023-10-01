#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>
#include <string>
#include <errno.h>


int main()
{
    // Create a socket
    int listening = socket(AF_INET, SOCK_STREAM, 0);
    if (listening == -1)
    {
        fprintf(stderr, "socket() failed: %s\n", strerror(errno));
        return -1;
    }

    // Bind socket to IP / Port
    sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(54000);
    inet_pton(AF_INET, "0.0.0.0", &server.sin_addr);

    if (bind(listening, (sockaddr*)&server, sizeof(server)) == -1)
    {
        fprintf(stderr, "bind() failed: %s\n", strerror(errno));
        return -2;
    }

    // Mark the socket for listening
    if (listen(listening, SOMAXCONN) == -1)
    {
        fprintf(stderr, "listen() failed: %s\n", strerror(errno));
        return -3;
    }

    // Accept a call
    sockaddr_in client;
    socklen_t clientSize = sizeof(client);
    char host[NI_MAXHOST];
    char svc[NI_MAXSERV];

    int clientSocket = accept(listening, (sockaddr*)&client, &clientSize);
    if (clientSocket == -1)
    {
        fprintf(stderr, "accept() failed: %s\n", strerror(errno));
        return -4;
    }

    // Close listening socket
    close(listening);

    memset(host, 0, NI_MAXHOST);
    memset(svc, 0, NI_MAXSERV);

    int result = getnameinfo(
        (sockaddr*)&client,
        clientSize,
        host,
        NI_MAXHOST,
        svc,
        NI_MAXSERV,
        0
        );

    if (result)
    {
        std::cout << host << " connected on " << svc << std::endl;
    }
    else
    {
        inet_ntop(AF_INET, &client.sin_addr, host, NI_MAXHOST);
        std::cout << " connected on " << ntohs(client.sin_port) << std::endl;
    }

    // Display message while receiving
    char buf[4096];
    while (true)
    {
        // Clear the buffer
        memset(buf, 0, 4096);
        // Wait for a message
        int bytesRecv = recv(clientSocket, buf, 4096, 0);
        if (bytesRecv == -1)
        {
            // Unexpected disconnect
            fprintf(stderr, "Connection issue: %s\n", strerror(errno));
            break;
        }
        if (bytesRecv == 0)
        {
            // Normal disconnect
            std::cout << "Client disconnected." << std::endl;
            break;
        }
        // Echo received message
        std::cout << "Received: " << std::string(buf, 0, bytesRecv) << std::endl;
        // Resend message
        send(clientSocket, buf, bytesRecv + 1, 0);
    }

    // Close client socket
    close(clientSocket);

    return 0;
}