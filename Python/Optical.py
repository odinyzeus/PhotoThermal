#!/usr/bin/python

from math import exp , log10

class Transmittance():
    """
    This class allow save or calculate the Optical Transmittance Value

    Parameters  :
        value   :   represent the Transmittance value directly assigned
        I       :   represent the Light's intensity array used to Transmittance calculate, with this form
                    [Initial,Final], both values must be float numbers 
        B       :   Represent the Optical Absorption Coefficient Value
        X       :   Represent the Optical Length that ligth must be cross through the sample
        Miu     :   Represent the Optical Penetration Depth of the sample

    Returns:
        Transmittance: Contains all necessary properties to calculate the optical transmittance value
    """

    __v     = 0.0       # Represents the Optical Transmittance Value
    __I     = [1.0,0.5] # Represents the Light's Intensity values present in the experiment
    __B     = 0.0       # Represents the Optical Absorption Coefficient of the sample
    __X     = 1e-2      # Represents the Optical Length that the light must be cross through the sample
    __m     = 0.0       # Represents the Optical depth penetration coefficient of the sample

    beta  = False
    length= False
    miu   = False
    intensity=False

    __calculateByI = lambda s : s.__I[1] / s.__I[0]
    __calculateByB = lambda s : exp(- s.Beta * s.__X)

    def reset(self):
        self.beta = False
        self.length = False
        self.miu = False
        self.intensity = False

    def __init__(self, value = 0.0, **kw) -> None:
        if value > 0.0:
            self.__v = value
        if 'I' in kw:
            self.__I = kw['I']
            self.intensity = True
        if 'B' in kw:
            self.__B = kw['B']
            self.beta = True
        if 'X' in kw:
            self.__X = kw['X']
            self.length = True
        if 'Miu' in kw:
            self.__m = kw['Miu']
            self.miu = True

    def __str__(self) -> str:
        return f'Depth = {self.Depth}\nLength = {self.Length}\nBeta = {self.Beta}\nInitial Intensity = {self.Intensity[0]}\nFinal Intensity = {self.Intensity[1]}\nTransmittance = {self.Transmittance}'

    @property
    def Depth(self):    # Return the penetration depth coefficient of the sample
        if self.miu:
            return self.__m
        if self.beta:
            return 1 / self.Beta

    @Depth.setter       # Set the penetration depth coefficient value of the sample 
    def Depth(self , d):
        self.__m = d
        self.miu = True
    
    @property           # Return the optical length that ligth must be cross through the sample
    def Length(self):
        return self.__X

    @Length.setter      # Set the optical length that ligth must be cross through the sample 
    def Length(self,X):
        self.__X = X
        self.length = True

    @property           # Return the Optical Absorption coefficient value   
    def Beta(self):
        if self.beta:
            return self.__B
        if self.miu:
            return 1 / self.__m
    
    @Beta.setter        # Set the Optical Absorption coefficient value
    def Beta(self,B):   
        self.__B = B
        self.beta = True

    @property           # Return the Light's Intensity using to Transmittance calculate
    def Intensity(self):
        return self.__I

    @Intensity.setter   # Set the Light's Intensity using to Transmittance calculate 
    def Intensity(self , I):
        self.__I = I
        self.intensity = True

    @property           # Return the Transmittance Value
    def Transmittance(self):
        if self.beta and self.length:
            self.__v = self.__calculateByB()
        if self.miu and self.length:
            self.__B = 1 / self.__m
            self.__v = self.__calculateByB()
        if self.intensity:
            self.__v = self.__calculateByI()
        return self.__v
    
    @Transmittance.setter       # Set the Transmittance value
    def Transmittance(self, v):
        self.__v = v
        self.reset()

class Absorbance(Transmittance):
    """ 
    This class allow save or calculate the Optical Absorbance Value

    Parameters  :
        value   :   represent the Optical Absorbance value directly assigned
        T       :   Could be represent it at two forms:
                    T = float value: Represent the Optical Transmittance value directly assigned
                    or a transmittance object

                    Example:
                    T = 0.8
                    or
                    T = Transmittance(I = [Initial,Final], B = 0.0, X = 0.0)
 
    Returns:
        Absorbance: Contains all necessary properties to calculate the optical Absorbance value
    """

    __v = 0.0           # This value represent the absorbance property

    __tx = False

    __calculateByT = lambda s : - log10( 1 / s.Transmittance)
    __calculateByB = lambda s : 0.43 * s.Beta * s.Length
    __beta         = lambda s : s.__v / (0.43 * s.Length)

    def __init__(self, Value = 0.0, **kw) -> None:
        if Value > 0.0:
            self.Absorbance = Value
        if 'T' in kw:
            self.Beta = kw['T'].Beta
            self.Depth = kw['T'].Depth
            self.Intensity = kw['T'].Intensity
            self.Length = kw['T'].Length
            if kw['T'].Transmittance != 0.0:
                self.Transmittance = kw['T'].Transmittance
                self.__tx = True
            self.beta = self.Beta is not None
            self.length = self.Length != 0.0

    def __str__(self) -> str:
        return super().__str__() + f'\nAbsorbance = {self.Absorbance}'

    @property           # Return the absorbance value
    def Absorbance(self):
        if self.__tx:
            self.__v = self.__calculateByT()
        if self.beta and self.length:
            self.__v = self.__calculateByB()

        return self.__v
    
    @Absorbance.setter       # Set the absorbance value
    def Absorbance(self , v):
        self.__v = v
        self.Beta = self.__beta()
        self.__tx = False
        
        
        
class Absorptance(Absorbance):
    """ 
    This class allow save or calculate the Fractional Optical Absorbance Value

    Parameters  :
        value   :   represent the Fractional Optical Absorbance value directly assigned
        A       :   Represent the Absorbance value and could be expressed it at two forms:
                    A = float value: Represent the Optical Absorbance value directly assigned
                    or 
                    A = class Absorbance object
                
    Returns:
        Absorptance: Contains all necessary properties to calculate the fractional optical Absorbance value
    """
    __v  = 0.0         # This represent the optical fractional absorbance or absorptance
  
    __calculate_a = lambda s : 1- s.Transmittance 

    def __init__(self, value = 0.0, **kw) -> None:
        if value != 0.0:
            self.__v = value

        if 'A' in kw:
            if type(kw['A']) is float:
                self.Absorbance = kw['A']

            if type(kw['A']) is Absorbance:
                self.Transmittance = kw['A'].Transmittance
                self.Absorbance = kw['A'].Absorbance

    def __str__(self) -> str:
        return super().__str__() + f'\nAbsorptance = {self.Absorptance}'

    @property
    def Absorptance(self):
        if self.Transmittance != 0.0:
            self.__v = self.__calculate_a()
        return self.__v

    @Absorptance.setter
    def Absorptance(self , a):
        self.__v = a

def main():
    __t = Transmittance(value=0.3) 
    __at = Absorbance(T = __t)
    __aa = Absorptance(A = __at)
    print(__aa)
    
if __name__ == '__main__':
    main()