# pygalfit
AriAstro - GALFIT

Workdir - https://github.com/Schwarzam/ariastro

Original -> Schwarzam/ariastro

2nd Column Description:

0 - Do not fit, do not adjust anything
1 - Best among the bands given, weighted mean 
2 - Parameter change linearly among bands

Above (degrees of freedom)
3 - Magnitudes (Pure measeure) degrees of freedom
for 5 bands put 5 
for 12 bands put 8


They need to follow the order of the wavelenghts.

People choose the object and object size.


- [ ] C - sigma image, may be made with weight images
- [ ] F - May be created with weight images
- [ ] H - Make it user input 
- [ ] I - 6-10x times FWMH of the psf image of the image —> S-plus would be 60 or 40


- [ ] Component 1: sky
- [ ] 1 - should be 0 the sky background

- [ ] Sersic
- [ ] 4 - R_e - KRON RAdius / 2 (guess) 
- [ ] 5 - Sersic index good to start with 4
- [ ] 9 - Axis ratio - KU - CU
- [ ] 10 - Position angle - PA


- [ ] EXPDISK 
- [ ] From R_e we can get R_s 

We may run a first run for sersic and then adjust it to others


Functions:
- Sersic
- Expdisk
- Moffat
- Ferrer
- Psf
- Sky 


Negative pixels in the image -> check if there are negative values and choose to maybe put them equal to 0. 


