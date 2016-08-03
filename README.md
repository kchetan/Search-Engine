# Erviz

The README is used to introduce the module and provide instructions on
how to install the module, any machine dependencies it may have (for
example C compilers and installed libraries) and any other information
that should be provided before the module is installed.

A README file is required for CPAN modules since CPAN extracts the README
file from a module distribution so that people browsing the archive
can use it to get an idea of the module's uses. It is usually a good idea
to provide version information here so that people can decide whether
fixes for the module are worth downloading.


## INSTALLATION

To install this module, run the following commands:

	`perl Makefile.PL`
	`make`
	`make test`
	`make install`

## SUPPORT AND DOCUMENTATION

After installing, you can find documentation for this module with the
perldoc command.

    `perldoc Erviz`

### You can also look for information at:

+ RT, CPAN's request tracker
        http://rt.cpan.org/NoAuth/Bugs.html?Dist=Erviz

+ AnnoCPAN, Annotated CPAN documentation
        http://annocpan.org/dist/Erviz

+ CPAN Ratings
        http://cpanratings.perl.org/d/Erviz

+ Search CPAN
        http://search.cpan.org/dist/Erviz/


## LICENSE AND COPYRIGHT

`Copyright (C) 2011 Gabriel Andrade`

This program is free software; you can redistribute it and/or modify it
under the terms of either: the GNU General Public License as published
by the Free Software Foundation; or the Artistic License.

See `http://dev.perl.org/licenses/` for more information.



# Wiki Search Engine 

## Instructions 

+ Two empty folders Index and Tindex should be present.
+ The input is an xml file as which is of the structure as shown in ./src/s.xml
+ the file assignment_index.py is for index file creating (merge sorted chunk)
+ the file assignment_sindex.py is for creating secondary index file
+ the file assignment_sindex_title.py is for creating secondary index file for the title
+ the file assignment_query.py is for getting the outputs for the query

## Running the code

Run the run.sh file with an input path of the xml file and the index file path as command line arguments.
nltk should be installed 
