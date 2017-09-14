/*
	Week8_PCAP_Programming
	201423044
	SeungHwan-Lee 
*/
#include "capture.h"

int setcolor(char *color)
{
	FILE *pp;
	char *line;
	char buf[1000];

	pp = popen(color, "r");

	if(pp != NULL)
	{
		while(1)
		{
			line = fgets(buf, sizeof(buf), pp);

			if(line == NULL) break;
			line[strlen(line)-1] = '\0';
			printf("%s", line);
		}
		pclose(pp);
	}

	return 0;
}
