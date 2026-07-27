# Independent evidence exporter for the KOU-21.137 candidate.
#
# This script deliberately exports only catalog metadata, a deterministic
# element indexing, the Cayley table, and square indices. All mathematical
# checks are performed by verify_cayley_certificate.py.

PrintIntegerList := function(values)
    local i;
    Print("[");
    for i in [1 .. Length(values)] do
        if i > 1 then
            Print(",");
        fi;
        Print(values[i]);
    od;
    Print("]");
end;;

G := SmallGroup(128, 928);;
elements := Elements(G);;
package_info := PackageInfo("smallgrp");;
identity_index := Position(elements, One(G)) - 1;;
generator_indices := List(
    GeneratorsOfGroup(G),
    generator -> Position(elements, generator) - 1
);;
square_indices := List(
    elements,
    element -> Position(elements, element * element) - 1
);;

Print("{");
Print("\"schema\":\"amra.cayley-export.v1\",");
Print("\"catalog\":{");
Print("\"name\":\"GAP SmallGroups Library\",");
Print("\"id\":[128,928],");
Print("\"constructor\":\"SmallGroup(128,928)\",");
Print("\"gap_version\":\"", GAPInfo.Version, "\",");
Print("\"smallgrp_package_version\":\"", package_info[1].Version, "\",");
Print("\"structure_description\":\"", StructureDescription(G), "\"");
Print("},");
Print("\"element_indexing\":{");
Print("\"basis\":\"zero-based position in GAP Elements(SmallGroup(128,928))\",");
Print("\"count\":", Length(elements), ",");
Print("\"identity_index\":", identity_index, ",");
Print("\"generator_indices\":");
PrintIntegerList(generator_indices);
Print("},");
Print("\"square_indices\":");
PrintIntegerList(square_indices);
Print(",\"cayley_table\":[");
for i in [1 .. Length(elements)] do
    if i > 1 then
        Print(",");
    fi;
    row := List(
        elements,
        right -> Position(elements, elements[i] * right) - 1
    );;
    PrintIntegerList(row);
od;
Print("]}");
Print("\n");

QUIT;
