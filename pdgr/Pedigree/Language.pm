=pod

=head1 NAME

Pedigree::Language - encapsulating language issues for pedigree library

=head1 SYNOPSIS

use Pedigree::Language;

$lang = new Pedigree::Language(I<$language>[, I<$encoding>]);

$lang->Header();

$lang->Language();

$lang->Encoding();

$lang->GetFieldNames();

$lang->GetValues();

$lang->GetSpecialNames();

$lang->PrintField(I<$field>, $<$value>);


=head1 DESCRIPTION

This package defines the language-dependent parts of the pedigree
library.  The idea is to gather everything about language here, so adding
a new language should be (presumably) be easy.

=over 4

=cut

####################################################################
# Define the package                                               #
####################################################################

package Pedigree::Language;
use strict;

#
# And package methods
#


####################################################################
#    new                                                           #
####################################################################

=pod


=item B<new>(I<$language>[, I<$encoding>]);

Construct the new interpreter from the given language and encoding names.

=cut


sub new {
    my $self={};
    my ($class,$language,$encoding)=@_;
    $self->{'language'}=$language;
    if (!defined($encoding) && ($language eq 'russian')) {
	$encoding='cp1251';
    }
    if (defined($encoding)) {
	$self->{encoding}=$encoding;
    }
    bless $self, $class;
    return ($self);
}


####################################################################
#    Header                                                        #
####################################################################


=pod

=item B<Header> ()

Print the language-related lines of the document preamble

=cut

sub Header {
    my $self=shift;
    my $result;
    if ($self->Encoding()) {
	$result .= '\usepackage['.$self->Encoding().']{inputenc}'."\n";
    }
    if (!($self->Language() eq 'english')) {
	$result .= '\usepackage['.$self->Language().']{babel}'."\n";
    }
    return $result;

}


####################################################################
#    Language                                                      #
####################################################################


=pod

=item B<Language> ()

Print the current language

=cut

sub Language {
    my $self=shift;
    return $self->{'language'};
}

####################################################################
#    Encoding                                                      #
####################################################################


=pod

=item B<Encoding> ()

Print the current encoding

=cut

sub Encoding {
    my $self=shift;
    return $self->{'encoding'};
}


####################################################################
#    GetFieldNames                                                 #
####################################################################


=pod

=item B<GetFieldNames>();

Outputs  a reference to a hash
"field_name_in_this_language"=>"field_name_in_English"

=cut

sub GetFieldNames() {
    my $self=shift;
    my %result=();
    
    #
    # The English names are default
    #
    %result=(
	     'Id'=>'Id',
	     'Name'=>'Name',
	     'Sex'=>'Sex',
	     'DoB'=>'DoB',
	     'DoD'=>'DoD',
	     'Mother'=>'Mother',
	     'Father'=>'Father',
	     'Proband'=>'Proband',
	     'Condition'=>'Condition',
	     'Type'=>'Type',
	     'Twins'=>'Twins',
	     'Comment'=>'Comment',
	     'SortOrder'=>'SortOrder',
	     'Sort'=>'SortOrder');

    #
    # Russian names depend on the encoding
    #
    if (($self->Language() eq 'russian') && ($self->Encoding() eq 'koi8-r')) {
	$result{'�����'}='Id';
	$result{'���'}='Name';
	$result{'���'}='Sex';
	$result{'����'}='DoB';
	$result{'����'}='DoD';
	$result{'����'}='Mother';
	$result{'����'}='Father';
	$result{'�������'}='Proband';
	$result{'���������'}='Condition';
	$result{'���'}='Type';
	$result{'��������'}='Twins';
	$result{'�����������'}='Comment';
	$result{'�����������������'}='SortOrder';
	$result{'����'}='SortOrder';
    }
    if (($self->Language() eq 'russian') && ($self->Encoding() eq 'cp1251')) {
	$result{'�����'}='Id';
	$result{'���'}='Name';
	$result{'���'}='Sex';
	$result{'����'}='DoB';
	$result{'����'}='DoD';
	$result{'����'}='Mother';
	$result{'����'}='Father';
	$result{'�������'}='Proband';
	$result{'���������'}='Condition';
	$result{'���'}='Type';
	$result{'��������'}='Twins';
	$result{'�����������'}='Comment';
	$result{'�����������������'}='SortOrder';
	$result{'����'}='SortOrder';
    }


    return \%result;
}

####################################################################
#    GetValues                                                     #
####################################################################


=pod

=item B<GetValues>();

Outputs  a reference to a hash
"field_value_in_this_language"=>"field_value_in_English"

=cut

sub GetValues {
    my $self=shift;
    my %result=();
    
    #
    # The English values are default
    #
    %result=(
	     'male'=>'male',
	     'female'=>'female',
	     'unknown'=>'unknown',
	     'yes'=>1,
	     'no'=>0,
	     'normal'=>'normal',
	     'obligatory'=>'obligatory',
	     'oblig'=>'obligatory',
	     'asymptomatic'=>'asymptomatic',
	     'asymp'=>'asymptomatic',
	     'affected'=>'affected',
	     'affect'=>'affected',
	     'infertile'=>'infertile',
	     'Infertile'=>'infertile',
	     'sab'=>'sab',
	     'Sab'=>'sab',
	     'monozygotic'=>'monozygotic',
	     'monozygot'=>'monozygotic',
	     'qzygotic'=>'qzygotic',
	     'qzygot'=>'qzygotic',
	     '?'=>'qzygotic',
	     );

    #
    # Russian names depend on the encoding
    #
    if (($self->Language() eq 'russian') && ($self->Encoding() eq 'koi8-r')) {
	$result{'���'} = 'male';
	$result{'���'} = 'female';
	$result{'�'} = 'male';
	$result{'�'} = 'female';
	$result{'�����'} = 'unknown';
	$result{'����������'} = 'unknown';
	$result{'��'} = 1;
	$result{'���'} = 0;
	$result{'��'} = 1;
	$result{'���'} = 0;
	$result{'����'} = 'normal';
	$result{'������'} = 'normal';
	$result{'�������'} = 'obligatory';
	$result{'�����'} = 'asymptomatic';
	$result{'�����'} = 'affected';
	$result{'�����'} = 'affected';
	$result{'��������'} = 'infertile';
	$result{'�������'} = 'sab';
	$result{'���������'} = 'monozygotic';
	$result{'����������'} = 'monozygotic';
	$result{'�������'} = 'monozygotic';
	$result{'�����'} = '';
    }

    if (($self->Language() eq 'russian') && ($self->Encoding() eq 'cp1251')) {
	$result{'���'} = 'male';
	$result{'���'} = 'female';
	$result{'�'} = 'male';
	$result{'�'} = 'female';
	$result{'�����'} = 'unknown';
	$result{'����������'} = 'unknown';
	$result{'��'} = 1;
	$result{'���'} = 0;
	$result{'��'} = 1;
	$result{'���'} = 0;
	$result{'����'} = 'normal';
	$result{'������'} = 'normal';
	$result{'�������'} = 'obligatory';
	$result{'�����'} = 'asymptomatic';
	$result{'�����'} = 'affected';
	$result{'�����'} = 'affected';
	$result{'��������'} = 'infertile';
	$result{'�������'} = 'sab';
	$result{'���������'} = 'monozygotic';
	$result{'����������'} = 'monozygotic';
	$result{'�������'} = 'monozygotic';
	$result{'�����'} = '';
    }

    return \%result;
}

####################################################################
#    GetSpecialNames                                               #
####################################################################


=pod

=item B<GetSpecialNames>();

Some values for the 'Name' field start with C<#>.  They are special.
This subroutine outputs  a reference to a hash
"special_name_in_this_language"=>"special_name"

=cut

sub GetSpecialNames {
    my $self=shift;
    my %result=();
    
    #
    # The English values are default
    #
    %result=(
	     'abort'=>'abortion',
	     'childless'=>'childless',
	     );

    #
    # Russian names depend on the encoding
    #
    if (($self->Language() eq 'russian') && ($self->Encoding() eq 'koi8-r')) {
	$result{'�����'} = 'abortion';
	$result{'�������'} = 'childless';
    }

    if (($self->Language() eq 'russian') && ($self->Encoding() eq 'cp1251')) {
	$result{'�����'} = 'abortion';
	$result{'�������'} = 'childless';
    }

    return \%result;
}



####################################################################
#    PrintField                                                    #
####################################################################


=pod

=item B<PrintField>(I<$field>, I<$value>);

Formats the value I<$value> of the given field I<$field> according
to the rules of the given language.

=cut

sub PrintField {
    my $self=shift;
    my ($field, $value) = @_;

    
    #
    # The English values are default
    #

    if ($self->Language() eq 'english') {
	if ($field eq 'DoB' ) {
	    return "born: $value";
	}
	if ($field eq 'DoD' ) {
	    return "died: $value";
	}
	if ($field eq 'AgeAtDeath') {
	    return "age at death: $value";
	}
    }

    if ($self->Language() eq 'russian') {
	if ($value eq 'unknown') {
	    $value = '{\cyr\cyrn\cyre\cyri\cyrz\cyrv.}';
	}
	if ($field eq 'DoB' ) {
	    return '{\cyr\cyrr\cyro\cyrd.}'." $value";
	}
	if ($field eq 'DoD') {
	    return '{\cyr\cyru\cyrm.}'." $value";
	}
	if ($field eq 'AgeAtDeath') {
	    return '{\cyr\cyru\cyrm. \cyrv{} \cyrv\cyro\cyrz\cyrr. }'." $value";
	}
	#
	# Special name
	#
	if ($field eq 'Name' && $value eq 'abortion') {
	    return '{\cyr\cyra\cyrb\cyro\cyrr\cyrt}';
	}
    }


    #
    # The last resort
    #
    return $value;


}



####################################################################
#    THE END                                                       #
####################################################################


=pod

=back

=head1 ENVIRONMENT

The calling program should define B<$main::DEBUG> and set it to 0
or 1.

=head1 SEE ALSO

pedigree(1), Pedigree(3)

=head1  AUTHOR

Boris Veytsman, Leila Akhmadeeva, 2006, 2007



=cut

1;
