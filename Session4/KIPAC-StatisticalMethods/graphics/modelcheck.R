open.png = function(name, width=3.05, height=2.8, units='in', resolution=300, points=9, xmin=0.15,xmax=0.99,ymin=0.17,ymax=0.99,plt=c(xmin,xmax,ymin,ymax), mgp=c(2.2,1,0), pch=".", ...) {
 png(name, width=width, height=height, pointsize=points, units=units, res=resolution)
 par(plt=plt, mgp=mgp, pch=pch, ...)
}



open.png('modelcheck-chisq.png', resolution=200, height=2.5, ymin=0.2, xmax=0.98, ymax=0.96, xmin=0.18)
curve(dchisq(x, 28), 0, 150, ylab=expression(P(chi^2*group("|",nu==28,""))), xlab=expression(chi^2))
abline(v=104.2, lty=2, col=4)
dev.off()

