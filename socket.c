#include <sys/socket.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <time.h>

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

	// char lantitude[] = "3150.42774 ";
	// char longtitude[] = "11715.11010";
	char *ch[5] = {"loc_state:A\n\
				Lat:3150.45775\n\
				Lat_NS:N\n\
				Lon:11715.13750\n\
				Lon_EW:E\n","loc_state:A\n\
				Lat:3150.45775\n\
				Lat_NS:N\n\
				Lon:11715.40750\n\
				Lon_EW:E\n","loc_state:A\n\
				Lat:3150.65775\n\
				Lat_NS:N\n\
				Lon:11715.40750\n\
				Lon_EW:E\n","loc_state:A\n\
				Lat:3150.95775\n\
				Lat_NS:N\n\
				Lon:11715.40750\n\
				Lon_EW:E\n","loc_state:A\n\
				Lat:3150.95775\n\
				Lat_NS:N\n\
				Lon:11715.30750\n\
				Lon_EW:E\n"};
	//for (int i = 0; i < 5; ++i)
				int i = 0;
	while(1)
	{
		i = (i + 1) % 5;
		ret  = write(client_sock, ch[i], strlen(ch[i]) + 1);
		printf("%d\n%s\n",ret,ch[i]);
		sleep(2);
	}
// ret  = write(client_sock, &ch, strlen(ch) + 1);
// //	ret  = write(client_sock, longtitude, strlen(longtitude) + 1);
// 	printf("%d\n%s\n",ret,ch);
	close(client_sock);
}

int main(int argc, char const *argv[])
{
	client();
	return 0;
}