import inspect
from fate_torch.base import FateTorchLayer
from torch import optim
from fate_torch.torch_modules_extract.extract_pytorch_modules import extract_init_param, Required
from torch.optim.optimizer import required


def code_assembly(param, nn_class):

    para_str = ""
    non_default_param = ""
    init_str = """"""
    for k, v in param.items():

        if k == 'params':
            continue

        new_para = "\n        self.param_dict['{}'] = {}".format(k, k)
        init_str += new_para
        if type(v) == Required or v ==  required :
            non_default_param += str(k)
            non_default_param += ', '
            continue

        para_str += str(k)
        if type(v) == str:
            para_str += "='{}'".format(v)
        else:
            para_str += "={}".format(str(v))
        para_str += ', '

    para_str = non_default_param + para_str

    init_ = """
    def __init__(self, {}**kwargs):
        FateTorchOptimizer.__init__(self)
        self.param_dict.update(kwargs){}
        # optim.{}.__init__(self, **self.param_dict)
    """.format(para_str, init_str, nn_class, nn_class)

    code = """
class {}(FateTorchOptimizer):
        {}
    """.format(nn_class, init_)

    return code


if __name__ == '__main__':
    from torch.optim import SGD
    memb = inspect.getmembers(optim)

    module_str = """"""
    module_str += "from torch import optim\n\nfrom fate_torch.base import FateTorchOptimizer"
    for k, v in memb:
        if inspect.isclass(v) and k != 'Optimizer':
            param = extract_init_param(v)
            code = code_assembly(param, k)
            module_str += code

    open('../optim.py', 'w').write(module_str)



