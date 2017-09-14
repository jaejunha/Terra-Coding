/*
	Week8_PCAP_Programming
	201423044
	SeungHwan-Lee 
*/
#include "capture.h"

void packet_info (u_char *user, const struct pcap_pkthdr *h, const u_char *p)
{
	int 			i, ipos=0;	// counters
	unsigned short 	type;		// type field in ethernet frame
	double 			crnt_t;		// current time

	// set initial time
	if ( cpkNum == 0 ) 
		init_t = (double)h->ts.tv_sec + 0.000001*h->ts.tv_usec;

    if(user)
		pcap_dump(user, h, p);

	/* set color */

	if((type=p[12]<<8 | p[13]) == 0x0800)	
	{
		setcolor(YELLO);
		if(p[23]==IP_PROTO_TCP)			setcolor(BLUE);
		else if(p[23]==IP_PROTO_UDP)			setcolor(PURPLE);
	}else								setcolor(RED);

     //printf("(%4d) clen=%3d, len=%4d \r",cpkNum++,h->caplen,h->len);
	// current time compared to the initial time
	crnt_t = (double)h->ts.tv_sec + 0.000001*h->ts.tv_usec;
	printf("%9.4f: [",crnt_t-init_t);

	// source MAC address
	for ( i=0; i<6; i++)    printf("%02x%s",p[i+6],i==5 ? "->" : ":") ;

	// destination MAC address
	for ( i=0;i<6;i++)   printf("%02x%s",p[i],i==5? "]": ":");

	// IP datagram
	if ( (type=p[12]<<8 | p[13]) == 0x0800 )
	{
		printf("(");
		// source IP address
		for ( i=0; i<4; i++)
			printf("%02d%s",p[i+26], i==3?"->":".");

		// destination IP address 
		for ( i=0; i<4; i++)
			printf("%02d%s",p[i+30], i==3?")":".");

		// upper layer protocol
		printf("%s", p[23]==IP_PROTO_TCP? "TCP":
			p[23]==IP_PROTO_UDP? "UDP":"OTH");
	}
	else
		printf("(Non-IP)");
	
	printf("\n");
	setcolor(RESET_BG);
    // store captured packet with WinPcap packet header
    


	//if ( cpkNum++ > MAXPKT ) {

	cpkNum++;

	if ( cpkNum == maxPkt ) 
	{
    	setcolor(RESET_BG);

		// close all devices and files
		pcap_close(adhandle);
        	
        	if(user){
        		pcap_dump_close((pcap_dumper_t *)user);
				makeStat();
			}

		exit(0);
	}
}
