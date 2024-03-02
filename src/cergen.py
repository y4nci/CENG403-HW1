import random
import math
from typing import Union

class gergen:
    pass

######################################################################
#------------------------- HELPER FUNCTIONS -------------------------#
######################################################################
def create_nested_list(boyut: tuple, aralik_list: list, current_dimension_idx: int, use_integer: bool) -> list:
    current_dimension = boyut[current_dimension_idx]

    if current_dimension == 0:
        raise ValueError('Dimension should be greater than 0')

    if current_dimension_idx == len(boyut) - 1:
        return [
            random.randint(*aralik_list) if use_integer else random.uniform(*aralik_list)
                for _ in range(current_dimension)
        ]
    
    return [create_nested_list(boyut, aralik_list, current_dimension_idx + 1, use_integer) for _ in range(current_dimension)]


######################################################################
#-------------------- FUNDAMENTAL FUNCTIONALITIES -------------------#
######################################################################
def cekirdek(sayi: int) -> None:
    """
    Sets the seed for random number generation to ensure reproducibility of results. Before generating random numbers (for instance,
    when initializing tensors with random values), you can call this function to set the seed.
    """
    random.seed(sayi)


def rastgele_dogal(boyut: tuple, aralik: tuple = (0, 100), dagilim='uniform') -> gergen:
    """
    Generates a gergen of specified dimensions with random integer values. The boyut parameter is a tuple specifying the dimensions of
    the gergen to be generated. The aralik parameter is an optional tuple (min, max) specifying the range of random values, with a 
    default range of (0, 100). The dagilim parameter specifies the distribution of random values, with ‘uniform’ as the default
    distribution. Possible values for dagilim include ‘uniform’ for a uniform distribution. You should raise ValueError if dagilim
    parameter is given differently.
    """

    if dagilim != 'uniform':
        raise ValueError('dagilim parameter should be uniform')
    
    aralik_list: list = list(aralik)

    # if boyut is 0, then we should return a scalar.
    if len(boyut) == 0:
        random_scalar = random.randint(*aralik_list)

        return gergen(random_scalar)

    return gergen(create_nested_list(boyut, aralik_list, 0, True))


def rastgele_gercek(boyut: tuple, aralik: tuple = (0.0,1.0), dagilim = None) -> gergen:
    """
    Generates a gergen of specified dimensions with random floating-point values. The boyut parameter is a tuple specifying the dimensions
    of the gergen to be generated. The aralik parameter is an optional tuple (min, max) specifying the range of random values, with a
    default range of (0.0,1.0). The dagilim parameter specifies the distribution of random values, with ‘uniform’ as the default
    distribution. Possible values for dagilim include ‘uniform’ for a uniform distribution. You should raise ValueError if dagilim
    parameter is given differently.
    """

    if dagilim != 'uniform':
        raise ValueError('dagilim parameter should be uniform')
    
    aralik_list: list = list(aralik)

    # if boyut is 0, then we should return a scalar.
    if len(boyut) == 0:
        random_scalar = random.uniform(*aralik_list)

        return gergen(random_scalar)
    
    return gergen(create_nested_list(boyut, aralik_list, 0, False))


class Operation:
    def __call__(self, *operands):
        """
        Makes an instance of the Operation class callable.
        Stores operands and initializes outputs to None.
        Invokes the forward pass of the operation with given operands.

        Parameters:
            *operands: Variable length operand list.

        Returns:
            The result of the forward pass of the operation.
        """
        self.operands = operands
        self.outputs = None
        return self.ileri(*operands)

    def ileri(self, *operands):
        """
        Defines the forward pass of the operation.
        Must be implemented by subclasses to perform the actual operation.

        Parameters:
            *operands: Variable length operand list.

        Raises:
            NotImplementedError: If not overridden in a subclass.
        """
        raise NotImplementedError


class gergen:

    __veri = None #A nested list of numbers representing the data
    D = None # Transpose of data
    __boyut = None #Dimensions of the derivative (Shape)


    def __init__(self, veri=None):
    # The constructor for the 'gergen' class.
    #
    # This method initializes a new instance of a gergen object. The gergen can be
    # initialized with data if provided; otherwise, it defaults to None, representing
    # an empty tensor.
    #
    # Parameters:
    # veri (int/float, list, list of lists, optional): A nested list of numbers that represents the
    # gergen data. The outer list contains rows, and each inner list contains the
    # elements of each row. If 'veri' is None, the tensor is initialized without data.
    #
    # Example:
    # To create a tensor with data, pass a nested list:
    # tensor = gergen([[1, 2, 3], [4, 5, 6]])
    #
    # To create an empty tensor, simply instantiate the class without arguments:
    # empty_tensor = gergen()
        self.__veri = veri
        pass

    def __getitem__(self, index):
    #Indexing for gergen objects
        pass

    def __str__(self):
        #Generates a string representation
        string_to_print = ""

        if self.__veri is None:
            string_to_print += "Boş gergen"

        elif type(self.__veri) == int or type(self.__veri) == float:
            # If the tensor is a scalar, we can directly return the string representation of the scalar.
            string_to_print += "0 boyutlu skaler gergen:\n" + str(self.__veri)

        else:
            current_nested_list = self.__veri

            # If the tensor is not a scalar, we need to iterate through the rows and columns to build the string representation.
            while True:
                if type(current_nested_list[0]) == int or type(current_nested_list[0]) == float:
                    string_to_print += str(len(current_nested_list))
                    break
                else:
                    string_to_print += str(len(current_nested_list)) + "x"
                    current_nested_list = current_nested_list[0]

            string_to_print += " boyutlu gergen\n" + str(self.__veri)

        return string_to_print


    def __mul__(self, other: Union['gergen', int, float]) -> 'gergen':
        """
        Multiplication operation for gergen objects.
        Called when a gergen object is multiplied by another, using the '*' operator.
        Could be element-wise multiplication or scalar multiplication, depending on the context.
        """
        pass

    def __truediv__(self, other: Union['gergen', int, float]) -> 'gergen':
        """
        Division operation for gergen objects.
        Called when a gergen object is divided by another, using the '/' operator.
        The operation is element-wise.
        """
        pass


    def __add__(self, other: Union['gergen', int, float]) -> 'gergen':
        """
        Defines the addition operation for gergen objects.
        Called when a gergen object is added to another, using the '+' operator.
        The operation is element-wise.
        """
        pass

    def __sub__(self, other: Union['gergen', int, float]) -> 'gergen':
        """
        Subtraction operation for gergen objects.
        Called when a gergen object is subtracted from another, using the '-' operator.
        The operation is element-wise.
        """
        pass

    def uzunluk(self):
    # Returns the total number of elements in the gergen
        pass

    def boyut(self):
    # Returns the shape of the gergen
        pass

    def devrik(self):
    # Returns the transpose of gergen
        pass

    def sin(self):
    #Calculates the sine of each element in the given `gergen`.
        pass

    def cos(self):
    #Calculates the cosine of each element in the given `gergen`.
        pass

    def tan(self):
    #Calculates the tangent of each element in the given `gergen`.
        pass

    def us(self, n: int):
    #Raises each element of the gergen object to the power 'n'. This is an element-wise operation.
        pass

    def log(self):
    #Applies the logarithm function to each element of the gergen object, using the base 10.
        pass

    def ln(self):
    #Applies the natural logarithm function to each element of the gergen object.
        pass

    def L1(self):
    # Calculates and returns the L1 norm
        pass

    def L2(self):
    # Calculates and returns the L2 norm
        pass

    def Lp(self, p):
    # Calculates and returns the Lp norm, where p should be positive integer
        pass

    def listeye(self):
    #Converts the gergen object into a list or a nested list, depending on its dimensions.
        pass

    def duzlestir(self):
    #Converts the gergen object's multi-dimensional structure into a 1D structure, effectively 'flattening' the object.
        pass

    def boyutlandir(self, yeni_boyut):
    #Reshapes the gergen object to a new shape 'yeni_boyut', which is specified as a tuple.
        pass

    def ic_carpim(self, other):
    #Calculates the inner (dot) product of this gergen object with another.
        pass

    def dis_carpim(self, other):
    #Calculates the outer product of this gergen object with another.
        pass
    def topla(self, eksen=None):
    #Sums up the elements of the gergen object, optionally along a specified axis 'eksen'.
        pass

    def ortalama(self, eksen=None):
    #Calculates the average of the elements of the gergen object, optionally along a specified axis 'eksen'.
        pass


    





















