/*
	Week8_PCAP_Programming
	201423044
	SeungHwan-Lee 
*/
#include "capture.h"

void cappkt_save (u_char *user, const struct pcap_pkthdr *h, const u_char *p)
{
	// display packet header information
	printf("(%4d) clen=%3d, len=%4d \r",cpkNum++,h->caplen,h->len);

	// store captured packet with WinPcap packet header
	pcap_dump(user, h, p);

	// check termination
	if ( cpkNum > MAXPKT ) {
		printf("\n\n %d-packets were captured ...\n", cpkNum);

		/* close all devices and files */
		pcap_close(adhandle);
		pcap_dump_close(pd);
		exit(0);
	}
}
