#!/usr/bin/awk -f

BEGIN { 
    FS=","; 
} 
{
    min=9999999999999;
    max=$3;
    for(i=4;i<=NF;i++){
        NUM=NUM?NUM+$i:$i;
        if ( $i < min ) {
            min=$i;
        }
        if ( $i > max ) {
            max=$i;
        }
    };
    $(NF+1)=NUM;
    print $1,$2,min,max,NUM/9; NUM=""  
}