#!/usr/bin/python
"""
this class permitt to get the values in determinated range from a completo data file.

"""
import pandas as pd , pathlib as pl

class Spectrum():
    __lambda    = 0.0
    __scale     = []
    __file      = r"spectrum.txt" 
    __path      = pl.Path().absolute()      # file that contains the actual absolute path
    __sp        = pd.DataFrame()

    __int2exp = lambda s,l : l * 1e-9
    __exp2int = lambda s,l : l / 1e-9

    def __init__(self, **kw) -> None:
        if 'Path' in kw:
            self.Path = kw['Path']

        if 'Scale' in kw:
            self.Scale = kw['Scale']
        else:
            self.Scale = [350,700,5]
        
        if 'File' in kw:
            self.File = kw['File']

        if 'Lambda' in kw:
            self.Lambda = kw['Lambda']
        else:
            self.Lambda = 400

    def __str__(self) -> str:
        return f'The spectrum values are Max:{self.Max}\tAverageDist:{self.meanDist}\tReferenceLambda:{self.Lambda}'

    @property
    def Scale(self):
        return self.__scale

    @Scale.setter
    def Scale(self,s):
        self.__scale = [x for x in range(s[0],s[1]+s[2],s[2])]
        self.__sp['Lambda'] = self.Scale

    @property
    def Lambda(self):
        return self.__lambda

    @Lambda.setter
    def Lambda(self , l):
        self.__lambda = self.__int2exp(l)

    @property
    def Path(self):
        return self.__path

    @Path.setter
    def Path(self , p):
        self.__path = p

    @property
    def File(self):
        return self.__file

    @File.setter
    def File(self, f):
        self.__file = f
        __t = pd.read_csv(f'{self.Path}/{f}', delimiter='\t', names= ['Lambda','Amplitude'], float_precision='round_trip')
        __t['Lambda'] = __t['Lambda'].astype(int)
        __t['Amplitude'] = __t['Amplitude'].astype(float)
        self.__sp['Amplitude'] = [__t.loc[__t['Lambda'] == l].Amplitude.mean() for l in [x for x in self.__sp['Lambda']]]

    def Save(self):
        self.Data.to_csv(f'{self.Path}/Spectrum.txt',sep='\t',index=False)

    @property
    def Max(self):
        __p = self.__sp.loc[self.__sp['Amplitude'] == self.__sp['Amplitude'].max()] 
        return int(__p.Lambda), float(__p.Amplitude)

    @property
    def Data(self):
        return self.__sp

    @property
    def meanDist(self):
        return sum([r.Lambda * r.Amplitude for idx, r in self.Data.iterrows()]) / sum([r.Amplitude for idx, r in self.Data.iterrows()])

def main():
    s = [400,700,5]
    l = 400
    sp = Spectrum(Scale = s, Lambda = l,File = 'absorbance.txt')
    print(sp)

if __name__ == '__main__':
    main()