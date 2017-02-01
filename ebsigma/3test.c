#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct genome{
	char* name;
	double found;
	double whole;
}Genome;

int main(int argc, char *argv[])
{
	char *delim = "\t";
	int i;
	char *buf = NULL;
	char *token;
	FILE* sigma_gvout;
	char *out1, *out2;
	FILE* found_out, * whole_out;
	Genome **gs;
	int gCount = 0;

	buf = (char*)malloc(sizeof(char)*1024);
	sigma_gvout = fopen(argv[1], "r");
	out1 = (char*)malloc(sizeof(char)*(strlen(argv[1])+10));
	out2 = (char*)malloc(sizeof(char)*(strlen(argv[1])+10));
	strcpy(out1, argv[1]);
	strcpy(out2, argv[1]);
	strcat(out1, "_krona1");
	strcat(out2, "_krona2");
	gs = (Genome**)malloc(sizeof(Genome*));
	found_out = fopen(out1, "w");
	whole_out = fopen(out2, "w");

	while(1)
	{
		fgets(buf, 1023, sigma_gvout);
		if(feof(sigma_gvout)) break;
//		printf("%s", buf);	//for check
		if(buf[0] == '@')
		{
			gCount++;
//			printf("%d\n", gCount);	//for check
			strtok(buf, delim);
			strtok(NULL, delim);
			token = strtok(NULL, delim);
//			printf("%s\n", token);	//for check
			gs = realloc(gs, gCount*sizeof(Genome*));
			gs[gCount-1] = (Genome*)malloc(sizeof(Genome));
			gs[gCount-1]->name = malloc((strlen(token)+1)*sizeof(char));
			strcpy(gs[gCount-1]->name, token);
			gs[gCount-1]->found = 0;
			gs[gCount-1]->whole = 0;
//			printf("%s\n", gs[gCount-1]->name);	//for check
		}
		if(buf[0] == '*')
		{
			strtok(buf, delim);
			token = strtok(NULL, delim);
			i = atoi(token);
			token = strtok(NULL, delim);
			gs[i]->found = atof(token);
			token = strtok(NULL, delim);
			gs[i]->whole = atof(token);
		}
	}

	gs = realloc(gs, (gCount+1)*sizeof(Genome*));
	gs[gCount] = (Genome*)malloc(sizeof(Genome));
	gs[gCount]->name = (char*)malloc(sizeof(char)*13);
	strcpy(gs[gCount]->name, "unclassified");
	gs[gCount]->found = 100;
	gs[gCount]->whole = 100;
	for(i=0;i<gCount;i++)
	{
		gs[gCount]->found-=gs[i]->found;
		gs[gCount]->whole-=gs[i]->whole;
	}
	for(i=0;i<gCount+1;i++)
	{
		if(gs[i]->found!=0)
			fprintf(found_out, "%f\t%s\n", gs[i]->found, gs[i]->name);
	}
	for(i=0;i<gCount+1;i++)
	{
		if(gs[i]->whole!=0)
			fprintf(whole_out, "%f\t%s\n", gs[i]->whole, gs[i]->name);
	}

	fclose(sigma_gvout);
	fclose(found_out);
	fclose(whole_out);
	free(buf);
	free(out1);
	free(out2);
	for(i=0;i<gCount;i++)
	{
		free(gs[i]->name);
		free(gs[i]);
	}
	free(gs);

	return 0;
}
