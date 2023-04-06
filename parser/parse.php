<?php

/**
 * IPP LS 2023
 * Projekt 1 - Skript pro parsovani zdrojoveho kodu v IPPcode23
 * Autor: Tomas Behal (xbehal02)
*/

ini_set('display_errors', 'stderr');

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/**
 * funkce pro kontrolu promenne
 * 
 * @param string $var
 * 
 * @return string
 */
function check_var($var){
    if (preg_match('/^(GF|TF|LF)@[ěščřžýáíéúůóďťňĚŠČŘŽÝÁÍÉÚŮÓĎŤŇa-zA-Z|_|-|\$|&|%|\*|\!|\?][ěščřžýáíéúůóďťňĚŠČŘŽÝÁÍÉÚŮÓĎŤŇa-zA-Z0-9|_|-|\$|&|%|\*|\!|\?]*$/', $var))
        return $var;
    else {
        fwrite(STDERR, "Error: Špatný formát proměnné (var)\n");
        exit(23);
    }
}

/**
 * funkce pro kontrolu konstanty nebo promenne
 * 
 * @param string $symb
 * 
 * @return string
 */
function check_symb($symb){
    if (preg_match('/^(GF|TF|LF)@[ěščřžýáíéúůóďťňĚŠČŘŽÝÁÍÉÚŮÓĎŤŇa-zA-Z|_|-|\$|&|%|\*|\!|\?][ěščřžýáíéúůóďťňĚŠČŘŽÝÁÍÉÚŮÓĎŤŇa-zA-Z0-9|_|-|\$|&|%|\*|\!|\?]*$/', $symb)) // var
        return $symb;
    else if (preg_match('/^int@([-+]?0$|([-+]?[1-9][0-9]+$|[-+]?[1-9][0-9]*(_[0-9]+)*$)|([-+]?0[xX][0-9a-fA-F]+(_[0-9a-fA-F]+)*$)|([-+]?0[oO]?[0-7]+(_[0-7]+)*$))/', $symb)) // int
        return explode('@', $symb,2)[1];
    else if (preg_match('/^bool@(true|false)$/', $symb)) // bool
        return explode('@', $symb,2)[1];
    else if (preg_match('/^string@([^\s#\\\\]|\\\\[0-9]{3})*$/', $symb)) // string
        return explode('@', $symb,2)[1];
    else if (preg_match('/^nil@nil$/', $symb)) // nil
        return explode('@', $symb)[1];
    else {
        fwrite(STDERR, "Error: Špatný formát konstanty nebo proměnné (symb)\n");
        exit(23);
    }
}

/**
 * funkce pro kontrolu navesti
 * 
 * @param string $label
 * 
 * @return string
 */
function check_label($label){
    if (preg_match('/^([a-zA-Z]|_|-|\$|&|%|\*|!|\?)([a-zA-Z]|_|-|\$|&|%|\*|!|\?|\d)*$/', $label)){
        return $label;
    }
    else {
        fwrite(STDERR, "Error: Špatný formát návěští(label)\n");
        exit(23);
    }
}

/**
 * funkce pro kontrolu typu
 * 
 * @param string $type
 * 
 * @return string 
 */
function check_type($type){
    if (preg_match('/^(int|bool|string)$/', $type))
        return $type;
    else
        fwrite(STDERR, "Error: Špatný formát typu (type)\n");
        exit(23);
}

/**
 * funkce pro zjisteni typu promenne ci konstanty
 * 
 * @param string $arg
 * 
 * @return string
 */
function get_symb_type($arg){
    if(preg_match('/^(GF|TF|LF)@/', $arg))
        return 'var';
    else if(preg_match('/^int@/', $arg))
        return 'int';
    else if(preg_match('/^bool@/', $arg))
        return 'bool';
    else if(preg_match('/^string@/', $arg))
        return 'string';
    else if(preg_match('/^nil@/', $arg))
        return 'nil';
    else
        fwrite(STDERR, "Error: Špatný formát konstanty nebo proměnné (symb)\n");
        exit(23);
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/**
 * main
 */

// kontrola argumentu z prikazove radky
if ($argc == 2){
    if ($argv[1] == "--help"){
        fwrite(STDOUT, "Použití: php8.1 parse.php [volitelný]\n\t [volitelný] --help\n\t Program bere ze standardního vstupu zdrojový kod IPPcode23.\n");
        exit(0);
    }
    else{
        fwrite(STDERR, "Error: Špatný parametr\n");
        exit(10);
    }
}
else if ($argc != 1){
    fwrite(STDERR, "Error: Špatný počet parametrů\n");
    exit(10);
}



// nactetni vstupu ze stdin a odstraneni komentaru a bilych znaku
$input = array();
while ($line = fgets(STDIN)) {
    $line = trim(preg_replace('/#.*/',' ', $line));
    $line = preg_replace('/\s+/', ' ', $line);
    if (empty($line)) continue;
    $input[] = $line;
}

// kontrola prazdneho vstupu
if (!isset($input[0]))
    exit(21);

// kontrola hlavicky
if (!(preg_match('/^.ippcode23$/i', $input[0]))) {
    fwrite(STDERR, "Error: Chybná nebo chybějící hlavička\n");
    exit(21);
}
else {
    array_shift($input);
}


// ulozeni vstupu do pole instrukci
$lines = array_map(function($line) {
    $line = explode(' ', $line);
    return array(
        'instruction' => $line[0],
        'args' => array_slice($line, 1)
    );
}, $input);


// priprava XML
$order = 1;

$xml = new XMLWriter();
$xml->openMemory();
$xml->setIndent(true);

$xml->startDocument('1.0', 'UTF-8');
$xml->startElement('program');
$xml->writeAttribute('language', 'IPPcode23');

// zpracovani instrukci a jejich argumentu
foreach ($lines as $line) {
    $xml->startElement('instruction');
    $xml->writeAttribute('order', $order);
    $xml->writeAttribute('opcode', strtoupper($line['instruction']));
    switch (strtoupper($line['instruction'])) {
        // simple
        case "CREATEFRAME":
        case "PUSHFRAME":
        case "POPFRAME":
        case "RETURN":
            if (count($line['args']) != 0) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }
            break;
        // var
        case 'DEFVAR':
        case 'POPS':
            if (count($line['args']) != 1) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }
            $xml->startElement('arg1');
            $xml->writeAttribute('type', 'var');
            $xml->text(check_var($line['args'][0]));
            $xml->fullEndElement();
            break;

        // var sym
        case "MOVE":
        case "INT2CHAR":
        case "STRLEN":
        case "TYPE":
        case "NOT":
            if (count($line['args']) != 2) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }
            $xml->startElement('arg1');
            $xml->writeAttribute('type', 'var');
            $xml->text(check_var($line['args'][0]));
            $xml->fullEndElement();
            $xml->startElement('arg2');
            $xml->writeAttribute('type', get_symb_type($line['args'][1]));
            $xml->text(check_symb($line['args'][1]));
            $xml->fullEndElement();
            break;
        // var sym sym
        case "ADD":
        case "SUB":
        case "MUL":
        case "IDIV":
        case "LT":
        case "GT":
        case "EQ":
        case "AND":
        case "OR":
        case "STRI2INT":
        case "CONCAT":
        case "GETCHAR":
        case "SETCHAR":
            if (count($line['args']) != 3) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }
            $xml->startElement('arg1');
            $xml->writeAttribute('type', 'var');
            $xml->text(check_var($line['args'][0]));
            $xml->fullEndElement();
            $xml->startElement('arg2');
            $xml->writeAttribute('type', get_symb_type($line['args'][1]));
            $xml->text(check_symb($line['args'][1]));
            $xml->fullEndElement();
            $xml->startElement('arg3');
            $xml->writeAttribute('type', get_symb_type($line['args'][2]));
            $xml->text(check_symb($line['args'][2]));
            $xml->fullEndElement();
            break;
        // sym
        case "PUSHS":
        case "WRITE":
            if (count($line['args']) != 1) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }
            $xml->startElement('arg1');
            $xml->writeAttribute('type', get_symb_type($line['args'][0]));
            $xml->text(check_symb($line['args'][0]));
            $xml->fullEndElement();
            break;
        // label
        case "CALL":
        case "LABEL":
        case "JUMP":
            if (count($line['args']) != 1) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }
            $xml->startElement('arg1');
            $xml->writeAttribute('type', 'label');
            $xml->text(check_label($line['args'][0]));
            $xml->fullEndElement();
            break;
        // label sym sym
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
            if (count($line['args']) != 3) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }

            $xml->startElement('arg1');
            $xml->writeAttribute('type', 'label');
            $xml->text(check_label($line['args'][0]));
            $xml->fullEndElement();
            $xml->startElement('arg2');
            $xml->writeAttribute('type', get_symb_type($line['args'][1]));
            $xml->text(check_symb($line['args'][1]));
            $xml->fullEndElement();
            $xml->startElement('arg3');
            $xml->writeAttribute('type', get_symb_type($line['args'][2]));
            $xml->text(check_symb($line['args'][2]));
            $xml->fullEndElement();
            break;
        // var type
        case "READ":
            if (count($line['args']) != 2) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }
            $xml->startElement('arg1');
            $xml->writeAttribute('type', 'var');
            $xml->text(check_var($line['args'][0]));
            $xml->fullEndElement();

            $xml->startElement('arg2');
            $xml->writeAttribute('type', 'type');
            $xml->text(check_type($line['args'][1]));
            $xml->fullEndElement();
            break;
        // spec symb
        case "EXIT":
        case "DPRINT":
            if (count($line['args']) != 1) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }
            $xml->startElement('arg1');
            $xml->writeAttribute('type', get_symb_type($line['args'][0]));
            $xml->text(check_symb($line['args'][0]));
            $xml->fullEndElement();
            break;
        case "BREAK":
            if (count($line['args']) != 0) {
                fwrite(STDERR, "Error: Špatný počet argumentů instrukce\n");
                exit(23);
            }
            fwrite(STDERR, "BREAK:" . $order . "\n");
            break;
        default:
            fwrite(STDERR, "Error: Neznámý nebo chybný operační kód\n");
            exit(22);
    }
    $xml->fullEndElement();
    $order++;
}
$xml->fullEndElement();
$xml->endDocument();
echo $xml->outputMemory();
?>
