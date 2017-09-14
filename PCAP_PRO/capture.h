/*
	Week8_PCAP_Programming
	201423044
	SeungHwan-Lee 
*/
#pragma once

#include <pcap.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "protocolHeader.h"	// it includes protocol(ethernet, ip, tcp, udp) structure info.

#define true 1
#define false 0

#define SNAPLEN				68		// size of captured packet (in bytes)
#define IP_PROTO_TCP		6		// TCP
#define IP_PROTO_UDP		17		// UDP

#define SNAPLEN         	68      // size of captured packet (in bytes)
#define MAXPKT          	2000    // maximum number of stored packets

#define FILE_NAME_MAX 		100		// The name of pkt file.

/* [CONSOLE BACKGROUND COLOR SET] */
#define RED			"bash -c 'echo -e \"\\033[41m\"'"
#define GREEN		"bash -c 'echo -e \"\\033[42m\"'"
#define YELLO		"bash -c 'echo -e \"\\033[43m\"'"
#define BLUE		"bash -c 'echo -e \"\\033[44m\"'"
#define PURPLE		"bash -c 'echo -e \"\\033[45m\"'"
#define WHITE		"bash -c 'echo -e \"\\033[47m\"'"
#define RESET_BG    "bash -c 'echo -e \"\\e[0m\"'"		// reset background color to default.

/* [SHIFTING MACRO] */
#define pntoh32(p)  ((unsigned short)*((unsigned char *)(p)+0)<<24|  \
                    (unsigned short)*((unsigned char *)(p)+1)<<16|  \
                    (unsigned short)*((unsigned char *)(p)+2)<<8|   \
                    (unsigned short)*((unsigned char *)(p)+3)<<0)

#define pntoh16(p)  ((unsigned short)                       \
                    ((unsigned short)*((unsigned char *)(p)+0)<<8|  \
                     (unsigned short)*((unsigned char *)(p)+1)<<0))

// call back function (disp)
void packet_info (u_char *user, const struct pcap_pkthdr *h, const u_char *p);

int setcolor(char *color);	// set command prompt's background color

void makeStat();	// make Statistics information from designated pkt file.

typedef int bool;	// it is just for c language.

int				cpkNum;		// counter for the number of captured packets
pcap_t			*adhandle;	// selected adaptor for packet capture
pcap_if_t		*alldevs;	// pointer for an adpator detected first
pcap_if_t		*d;			// pointer for available adaptors


double 			init_t; // for statistics

char			pktFileName[FILE_NAME_MAX]; // it is used only when user designates '-f' option.
int				maxPkt;
