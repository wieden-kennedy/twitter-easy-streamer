from setuptools import setup, find_packages

setup(
        name='twitter-easy-streamer',
        version='0.0.1',
        description='Easily stream tweets using tweepy',
        long_description=open('README.md').read(),
        author='Wieden+Kennedy',
        author_email='nilesh.ashra@wk.com',
        url='https://github.com/wieden-kennedy/twitter-easy-streamer/',
        packages=find_packages(),
        include_package_data=True,
        install_requires=['requests', 'tweepy'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
