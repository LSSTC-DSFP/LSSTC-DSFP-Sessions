open.png = function(name, width=3.05, height=2.8, units='in', resolution=300, points=9, xmin=0.15,xmax=0.99,ymin=0.17,ymax=0.99,plt=c(xmin,xmax,ymin,ymax), mgp=c(2.2,1,0), pch=".", ...) {
 png(name, width=width, height=height, pointsize=points, units=units, res=resolution)
 par(plt=plt, mgp=mgp, pch=pch, ...)
}

y = rexp(1000000)
yy = pmax(0, y + rnorm(length(y), 0, 0.5*sqrt(y))) # "Poisson-like" scatter

open.png('missing_eddington.png', resolution=200, height=2.5, ymin=0.2, xmax=0.98, ymax=0.98)
par(yaxs='i', xaxs='i')
h = hist(y, breaks=seq(0, ceiling(max(yy)), 0.2), xlim=c(2.6,8.5), col='lightskyblue', ylim=c(0,15000), xlab='L')
hist(yy[which(yy>=3)], breaks=h$breaks, add=T)
abline(v=3, lty=2)
box()
legend('topright', c('Complete sample, no scatter', 'L>3 sample, with scatter'), inset=0.02, pch=c(15, 22), col=c('skyblue', 1))
dev.off()


j = which(yy>=1.25)[1:50]
open.png('missing_eddington_0.png', resolution=200, height=2.5, ymin=0.2, xmax=0.98, ymax=0.98)
plot(y[j], xlab='Source number', ylab='L', pch=1, cex=0.8, col='blue')
abline(h=3, lty=2)
dev.off()
open.png('missing_eddington_1.png', resolution=200, height=2.5, ymin=0.2, xmax=0.98, ymax=0.98)
plot(yy[j], xlab='Source number', ylab='L', pch=20, col='blue')
abline(h=3, lty=2)
points(y[j], pch=1, cex=0.8, col='blue')
arrows(1:length(j), y[j], y1=yy[j], col='red', length=0.05)
dev.off()


