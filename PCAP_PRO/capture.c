/*
	Week8_PCAP_Programming
	201423044
	SeungHwan-Lee 
*/
#include "capture.h"

int main(int argc, char** argv)
{
	/* etc familiy */
	bool fileOption=false;

	/* disp familiy */
	char				errbuf[PCAP_ERRBUF_SIZE];
	int					i;			// for general use
	int					ndNum=0;	// number of network devices
	int					devNum;		// device Id used for online packet capture
    pcap_dumper_t       *pd;        // dump file pointer

	cpkNum = 0;

	switch(argc)
	{
		printf("# ARGC : %d \n", argc);
		case 1: // case of none-option
			maxPkt = MAXPKT;
			break;
		case 3: // case of write option
			if(!strcmp(argv[1], "-f")) 
			{
				strcpy(pktFileName, argv[2]);
				fileOption = true;
			}else if(!strcmp(argv[1], "-t"))
			{
				maxPkt = atoi(argv[2]);
			}else{
				fprintf(stderr, "option error \n");
				printf("%s [-f] [pktFileName.pkt] [-t] [number of max packet]\n", argv[0]);
				perror("");
				return -1;
			}
			break;
		case 5:
			if(!strcmp(argv[1], "-f") && !strcmp(argv[3], "-t")) 
			{
				strcpy(pktFileName, argv[2]);
				fileOption = true;
				maxPkt = atoi(argv[4]);
			}else if(!strcmp(argv[1], "-t") && !strcmp(argv[3], "-f"))
			{
				strcpy(pktFileName, argv[4]);
				fileOption = true;
				maxPkt = atoi(argv[2]);
			}else{
				fprintf(stderr, "Wrong Option!\n");
				printf("%s [pktFileName.pkt]\n", argv[0]);
				perror("");
				return -1;
			}
			break;
		default:
			fprintf(stderr, "Wrong Argument!\n");
			printf("%s [-f] [pktFileName.pkt] [-t] [number of max packet]\n", argv[0]);
			return -1;
	}

	 /* Retrieve the device list */
    if (pcap_findalldevs(&alldevs, errbuf) == -1)
    {
        fprintf(stderr,"Error in pcap_findalldevs: %s\n", errbuf);
        exit(1);
    }
    
    /* Print the list */
    for(d=alldevs; d; d=d->next)
    {
        printf("%d. %s", ++ndNum, d->name);
        if (d->description)
            printf(" (%s)\n", d->description);
        else
            printf(" (No description available)\n");

    }
    
    /* error ? */
    if(ndNum==0)
    {
        printf("\nNo interfaces found! Make sure WinPcap is installed.\n");
        return -1;
    }
    
    /* select device for online packet capture application */
    printf("Enter the interface number (1-%d):",ndNum);
    scanf("%d", &devNum);
    
    /* select error ? */
    if(devNum < 1 || devNum > ndNum)
    {
        printf("\nInterface number out of range.\n");
        /* Free the device list */
        pcap_freealldevs(alldevs);
        return -1;
    }
    
    /* Jump to the selected adapter */
    for(d=alldevs, i=0; i< devNum-1 ;d=d->next, i++);

    /* Open the adapter */
    if ( (adhandle= pcap_open_live(d->name,     // name of the device
                             SNAPLEN,           // captured packet size
                             1,                 // promiscous mode
                             1000,              // read timeout
                             errbuf             // error buffer
                             ) ) == NULL)
    {
        fprintf(stderr,"\nUnable to open the adapter. %s is not supported..\n",d->name);
        /* Free the device list */
        pcap_freealldevs(alldevs);
        return -1;
    }

    printf("\nselected device %s is available\n\n", d->description);
    
    /* At this point, we don't need any more the device list. Free it */
    pcap_freealldevs(alldevs);
    pd = NULL;
    if(fileOption==true)
	{
		pd = pcap_dump_open( adhandle, pktFileName);
		pcap_loop(adhandle, -1, packet_info, (u_char *)pd) ;
	}else{
 		pcap_loop(adhandle, -1, packet_info, NULL) ;
	}
	return 0;
}
