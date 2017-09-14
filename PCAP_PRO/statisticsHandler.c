/*
	Week8_PCAP_Programming
	201423044
	SeungHwan-Lee 
*/
#include "capture.h"

#include <pcap.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define LINE_LEN 			16

/* litereals realted to distinguishing protocols */
#define ETHERTYPE_IP		0x0800
#define ETH_II_HSIZE		14		// frame size of ethernet v2
#define ETH_802_HSIZE		22		// frame size of IEEE 802.3 ethernet
#define	RTPHDR_LEN			12		// Length of basic RTP header
#define CSRCID_LEN			4		// CSRC ID length
#define	EXTHDR_LEN			4		// Extension header length

unsigned long	net_ip_count;
unsigned long	net_etc_count;
unsigned long	trans_tcp_count;
unsigned long	trans_udp_count;
unsigned long	trans_etc_count;

unsigned long	maxPerSec;
unsigned long	minPerSec;

void do_ip_traffic_analysis(unsigned char *pktData)
{
	unsigned char ip_ver, ip_hdr_len, ip_proto;
	int	ip_offset=14;

	ip_ver 	= pktData[ip_offset]>>4;		// IP version
	ip_hdr_len 	= pktData[ip_offset] & 0x0f ;	// IP header length
	ip_proto 	= pktData[ip_offset + 9];		// protocol above IP

	if ( ip_proto == IP_PROTO_UDP )
		trans_udp_count++;
	else if ( ip_proto == IP_PROTO_TCP )
		 trans_tcp_count++;
	else
		 trans_etc_count++;
}

void do_traffic_analysis(unsigned char *pktData)
{
	unsigned short type;
	// ethernet type check
	type = pntoh16(&pktData[12]);

	if ( type == ETHERTYPE_IP )
	{
	 	net_ip_count++;
		do_ip_traffic_analysis(pktData) ;
	}
	else			
		net_etc_count++;
}

void display_TCP(unsigned char *pktData)
{
	tcp_header *th = (tcp_header *)(&pktData[34]);

	printf("[PORT] %d --> ", pktData[34] <<8| pktData[35]);
	printf("%d\n", pktData[36] <<8 | pktData[37]);
	printf("Seq Number: %u \n", pntoh32(&pktData[38]));
	printf("Ack Number: %u \n", pntoh32(&pktData[42]));
	printf("flag: %X\n", pktData[44] & 0x3F); // use 6 bits
	printf("Window: : %u \n", pntoh16(&pktData[45]));
	printf("checkSum: : %u\n", pntoh16(&pktData[46]));
	return;
}

void display_UDP(unsigned char *pktData)
{
	udp_header *uh = (udp_header *)(&pktData[34]);

	printf("[PORT] %u --> ", pktData[34] <<8| pktData[35]);
	printf("%u\n", pktData[36] <<8 | pktData[37]);
	printf("length: %u \n", pntoh16(&pktData[38]));
	printf("checkSum: %u \n", pntoh16(&pktData[40]));
	return;
}

void display_IP(unsigned char *pktData)
{
	ip_header *iph = (ip_header *)(&pktData[14]);
	struct sockaddr_in src, dst;

	src.sin_addr.s_addr = iph->srcAddr;
	dst.sin_addr.s_addr = iph->dstAddr;

	printf(" Version: %d\n", iph->VR_HL >> 4);
	printf(" Header Length: %d\n", iph->VR_HL & 0xF );
	printf(" Tos: %d\n", iph->Tos );
	printf(" length of Total: %d\n", iph->length );
	printf(" identification: %d\n", iph->id );
	printf(" TTL: %d\n", iph->TTL );
	printf(" Header checksum: %d\n", iph->Hchecksum );
	printf("[IP] %s -> ", inet_ntoa(src.sin_addr));
	printf("%s \n", inet_ntoa(dst.sin_addr));


	if(iph->protocol == IP_PROTO_TCP)
		display_TCP(pktData);	
	else if(iph->protocol == IP_PROTO_UDP)
		display_UDP(pktData);	
	else
		printf("LAYER-4 : ETC");

}

void display_ETHER(unsigned char *pktData)
{
	eth_header *ether=(eth_header *)(pktData);

	printf("[MAC] %02x:%02x:%02x:%02x:%02x;%02x -> %02x:%02x:%02x:%02x:%02x;%02x\n", 
			ether->srcMac.addr1,
			ether->srcMac.addr2,
			ether->srcMac.addr3,
			ether->srcMac.addr4,
			ether->srcMac.addr5,
			ether->srcMac.addr6,
			ether->dstMac.addr1,
			ether->dstMac.addr2,
			ether->dstMac.addr3,
			ether->dstMac.addr4,
			ether->dstMac.addr5,
			ether->dstMac.addr6);
	printf("Upper Layer code : %X\n", ether->type);

	return;
}

void display_packet_information(unsigned char *pktData)
{
	eth_header *ether=(eth_header *)(pktData);
	printf("===========================\n");

		display_ETHER(pktData);
	if ( ether->type == 0x0008 )
		display_IP(pktData); // index of 0~13 is already used.

	printf("===========================\n");


}

/* determine max/min packets per second. */
void determine_max_min_persec(long *currentTime, int last)
{
	static short 	pktCountPerSec=0;
	static long		prevTime=0;
	static short	init_s=0;
	
	if(prevTime==0)
		prevTime = *currentTime;
	
	++pktCountPerSec;
	if( *currentTime != prevTime || last==1 )
	{// if time moves to next second or it is last packet.
		prevTime = *currentTime;
		if(maxPerSec < pktCountPerSec)
			maxPerSec = pktCountPerSec;
		else if(minPerSec > pktCountPerSec)
			minPerSec = pktCountPerSec;

		if(init_s==0){
			minPerSec = pktCountPerSec;
			init_s=1;
		}
		pktCountPerSec = 0;
	}

	return;
}

void makeStat()
{
	struct pcap_file_header	fhdr;
	struct pcap_pkthdr 		chdr;
	unsigned char			pktData[262144];
	FILE					*fin;
	int						i=0;
	int						trans_packet;
	long					init_time=0, last_time=0, total_time; // represented by a second.

	fin = fopen(pktFileName, "rb");

	fread((char *)&fhdr, sizeof(fhdr), 1, fin);

	while ( fread((char *)&chdr, sizeof(chdr), 1, fin) != 0 ) // Packet header
	{
		if(init_time==0) init_time = chdr.ts.tv_sec;
		determine_max_min_persec(&(chdr.ts.tv_sec), 0);
		fread(pktData, sizeof(unsigned char), chdr.caplen, fin);
		display_packet_information(pktData);
		do_traffic_analysis(pktData);
		i++;
	}
	determine_max_min_persec(&(chdr.ts.tv_sec), 1);
	last_time = chdr.ts.tv_sec; // assign a last time.
	total_time = last_time - init_time;
	printf("TOTAL TIME : %d\n", total_time);

	fclose(fin);

	printf("========< STATISTICS INFORMATION >===========\n\n");
	printf("#Total number of packets : %d\n\n", i);

	printf("    [ NETWORK-LAYER INFORMATION ]\n\n");
	printf("1] IP     packets: %.2f%\n", (net_ip_count/(float)i)*100);
	printf("2] non-IP packets: %.2f%\n\n", (net_etc_count/(float)i)*100);
	
	trans_packet = trans_tcp_count + trans_udp_count + trans_etc_count;
	printf("    [ TRANSPORT-LAYER INFORMATION ]\n\n");
	if(trans_packet <= 0)
	{
		printf("#[DEBUG Msg] transport layer protocol was not detected.\n");
	}else{
		printf("1] TCP packets: %.2f%\n", (trans_tcp_count/(float)trans_packet)*100);
		printf("2] UDP packets: %.2f%\n", (trans_udp_count/(float)trans_packet)*100);
		printf("3] OTH packets: %.2f%\n", (trans_etc_count/(float)trans_packet)*100);
	}
	
	printf("    [ PACKETS PER SECONDS ]\n\n");
	printf("1] Average packet per second: %.2f\n", i/(float)total_time);
	printf("2] Maximum packet per second: %d\n", maxPerSec);
	printf("3] Minimum packet per second: %d\n", minPerSec);
	printf("=====================================\n");
	return;
}


