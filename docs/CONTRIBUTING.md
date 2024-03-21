# Developing Hotmart Python

## Notes

For some reason, when trying to install packages in test.pypi.org the dependecies for this package are being pulled also
from [test.pypi.org](https://test.pypi.org), which is not the expected behavior. This is causing the installation to fail. The main solution is
to use this command when installing: `pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ hotmart-python`