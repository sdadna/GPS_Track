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
	struct GPS
	{
		char lantitude[12];
		char longtitude[12];
	};
	 struct GPS GPS_Point;
	// GPS_Point = (struct GPS *)malloc(sizeof(struct GPS));
	// if(!GPS_Point){
	// 	perror("malloc error");
	// 	return -1;
	// }
	strncpy(GPS_Point.lantitude, "#11715.11010#", 14);
	strncpy(GPS_Point.longtitude, "#3150.42774#", 13);
	// char lantitude[] = "3150.42774 ";
	// char longtitude[] = "11715.11010";

	ret  = write(client_sock, &GPS_Point, sizeof(GPS_Point));
//	ret  = write(client_sock, longtitude, strlen(longtitude) + 1);
	printf("%d %f %f\n",ret, GPS_Point.lantitude, GPS_Point.longtitude);
	close(client_sock);
}

int main(int argc, char const *argv[])
{
	client();
	return 0;
}