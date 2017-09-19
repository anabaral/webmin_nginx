#!/usr/bin/perl
# edit_server.cgi
# Display a text box for manually editing directives

require './nginx-lib.pl';
&ReadParse();

my $dir = "$config{'virt_dir'}";
my $file = "$dir/$in{'editfile'}";
if (!-e $file) {
  $file = "$in{'editfile'}";
}
if (!-e $file) {
  $file = "$config{'nginx_dir'}/$in{'editfile'}";
}

&ui_print_header($title, $text{'manual_title'}, "");

if ( "$in('editfile')" =~ /.*default.conf.*/) {
	
	$template_file = "./edit_default_conf_template.html";

	# buf header, footer
	$lref = &read_file_lines($template_file);
	$is_head = 1;
	if (!defined($start_t)) {
		$start_t = 0;
		$end_t = @$lref - 1;
	}
	for($i=$start_t; $i<=$end_t; $i++) {
		$line_content = $lref->[$i];
		if ($line_content eq "#FILE_CONTENT#") {
			$is_head=0;
			next;
		}
		
		$key = '\${editfile}';
		$line_content =~ s/$key/$file/ ;
		
		if ($is_head == 1){
			$buf_head .= $line_content."\n";
		}else{
			$buf_tail .= $line_content."\n";
		}
	}
	
	# file content
	$lref = &read_file_lines($file);
	if (!defined($start)) {
		$start = 0;
		$end = @$lref - 1;
		}
	for($i=$start; $i<=$end; $i++) {
		$buf .= $lref->[$i]."\n";
		}
	print $buf_head;
	print $buf;
	print $buf_tail;
	
	&ui_print_footer("$return", "server listing");


} else {

	print &text('manual_header', "<tt>$file</tt>"),"<p>\n";
	
	# textbox form
	print &ui_form_start("edit_save.cgi", "form-data");
	print &ui_hidden("editfile", $file),"\n";
	
	$lref = &read_file_lines($file);
	if (!defined($start)) {
		$start = 0;
		$end = @$lref - 1;
		}
	for($i=$start; $i<=$end; $i++) {
		$buf .= $lref->[$i]."\n";
		}
	print &ui_textarea("directives", $buf, 25, 80, undef, undef,"style='width:100%'"),"<br>\n";
	print &ui_submit($text{'save'});
	print &ui_form_end();
	
	&ui_print_footer("$return", "server listing");


}

