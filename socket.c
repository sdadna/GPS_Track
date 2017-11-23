#include <sys/socket.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>

int client(){
	int client_sock;
	int ret;
	struct sockaddr_in serverAddr;

	if((client_sock = socket(AF_INET, SOCK_STREAM, 0)) < 0){
		perror("socket");
		return 1;
	}
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(9000);
	serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

	if(connect(client_sock, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0){
		perror("connect");
		return 1;
	}

	//char ch[] = "3";
	float lantitude = 3150.42774;
	float longtitude = 11715.11010;

	ret  = write(client_sock, &lantitude, sizeof(float));
	ret  = write(client_sock, &longtitude, sizeof(float));
	printf("%d %f %f\n",ret, lantitude, longtitude);
	close(client_sock);
}

int main(int argc, char const *argv[])
{
	client();
	return 0;
}