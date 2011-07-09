/***************************************************************************
 * (c) 2010 - file created by Colin Coe.
 *
 * You may choose any license of the current release or any future release
 * of editarea to use, modify and/or redistribute this file.
 *
 * This language specification file supports provides syntax checking for
 * builtin reserved words and commands.
 ***************************************************************************/

editAreaLoader.load_syntax["bash"] = {
	'DISPLAY_NAME' : 'BASH',
	'COMMENT_SINGLE' : {1 : '#'},
	'QUOTEMARKS' : {1: "'", 2: '"'},
	'KEYWORD_CASE_SENSITIVE' : true,
	'KEYWORDS' :
	{
		'core' :
			[ 
			"if", "then", "else", "elif", "while", "for",
			"do", "fi", "case", "esac", "done", "in", "select",
			"export", "set", "unset", "until", "function", "echo",
			"print", "printf", "cd", "mkdir", "rmdir", "bg", "fg",
			"trap", "umask"
			],
		'functions' :
			[
			"-a", "-b", "-c", "-d", "-e", "-f", "-g", "-h", "-k",
			"-p", "-r", "-s", "-t", "-u", "-w", "-x", "-O", "-G",
			"-L", "-S", "-S", "-N", "-nt", "-ot", "-ef", "-o",
			"-z", "-n"
			]
	},
	'OPERATORS' :
		[
		"==", "!=", "<", ">", "-eq", "-ne", "-lt", "-le", "-gt", "-ge"
		],
	'DELIMITERS' :
		[ '(', ')', '[', ']', '{', '}', '`', '[[', ']]', '((', '))' ],
/*	'REGEXPS' :
	{
		'packagedecl' : { 'search': '(package )([^ \r\n\t#;]*)()',
			'class' : 'scopingnames',
			'modifiers' : 'g', 'execute' : 'before' },
		'subdecl' : { 'search': '(sub )([^ \r\n\t#]*)()',
			'class' : 'scopingnames',
			'modifiers' : 'g', 'execute' : 'before' },
		'scalars' : { 'search': '()(\\\$[a-zA-Z0-9_:]*)()',
			'class' : 'vars',
			'modifiers' : 'g', 'execute' : 'after' },
		'arrays' : { 'search': '()(@[a-zA-Z0-9_:]*)()',
			'class' : 'vars',
			'modifiers' : 'g', 'execute' : 'after' },
		'hashs' : { 'search': '()(%[a-zA-Z0-9_:]*)()',
			'class' : 'vars',
			'modifiers' : 'g', 'execute' : 'after' },
	},
*/
	'STYLES' :
	{
		'COMMENTS': 'color: #AAAAAA;',
		'QUOTESMARKS': 'color: #DC0000;',
		'KEYWORDS' :
		{
			'core' : 'color: #8aca00;',
			'functions' : 'color: #2B60FF;'
		},
		'OPERATORS' : 'color: #8aca00;',
		'DELIMITERS' : 'color: #0038E1;'
/*		,'REGEXPS':

		{
			'scopingnames' : 'color: #ff0000;',
			'vars' : 'color: #00aaaa;',
		}
*/
	} //'STYLES'
};
