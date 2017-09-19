rm(list=ls())
graphics.off()
setwd("~/Desktop")
datos <- read.csv("full_data.csv")

p <- "P875"
duracion <- 38
sess <- c(1:41)
#evento <- 1
#datoos <- array(data=0,dim=c(20,30))
#datoos <- data.frame(datoos)
#ensayo <- 15
for(sess in 30:41){
  paloma <- which(datos$bird == p)
  paloma <- datos[paloma,]
  sesion <- which(paloma$data_file==paste0("M_PEAK",sess,p))
  sesion <- paloma[sesion,]
  
  a <- which(sesion$event==paste0("LDRP_ON_",duracion))
  b <- which(sesion$event==paste0("LDRP_OFF_",duracion))
  
  #datas = cbind(0,matrix(0,nrow = 100,ncol = 15))
  layout(matrix(1:6,ncol=2))
  par(mar=c(2,2,1,1),oma=c(3,3,2,0))
  
  
  for(ensayo in 1:length(a)) { 
    ver <- sesion[a[ensayo]:b[ensayo],]
    x <- ver[,12:13]
    respuesta <- paste0("Res_TDRP_",duracion)
    trespuestas <- which(ver$event==respuesta)
    
    n_red <- x[,2]-min(x[,2])
    t_norm <- floor(n_red)
    datos_p <- data.frame(x,n_red,t_norm)
    
    tiempo <- seq(0,max(datos_p$t_norm))
    n_seg <- rep(0,length(tiempo))
    res_seg <- data.frame(tiempo,n_seg)
    
    for(i in 0:length(res_seg$tiempo)){
      x1<- length(which(datos_p$t_norm==i & 
                          (datos_p$event==paste0("Res_TDRP_",duracion))))
      res_seg[i+1,2] <- x1
      
      # setwd("C:/Users/Uriel/Desktop/Palomas")
      write.csv(res_seg,paste0(p,"_",duracion,"_",ensayo,"_",sess,".csv",na=""))
      
    }
    plot(res_seg$tiempo,res_seg$n_seg,type="o",main=paste0("E",ensayo),pch=16,lwd=1.5,
         col="dimgray",lty="dashed",xlab="segundo",ylab="R/s")
    # plot(res_seg$tiempo,cumsum(res_seg$n_seg),type="s",main=paste0("Ensayo",ensayo),
    #      lwd=2,col="gray21")
    
  }
  
  mtext("Segundos",1,outer=T, cex = 1,line=1.5)
  mtext("Respuestas Acumuladas",2,outer=T, cex = 1,line=1.4)
}

#View(res_seg)






