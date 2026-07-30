# Raw, predicate-free Cayley-table exporter for KOU-21.137.
#
# The downstream Python verifier deliberately receives only catalogue
# coordinates and multiplication tables.  In particular, this exporter does
# not ask GAP for the exponent, the set of squares, subgroup closure, or
# commutativity.

SizeScreen([100000, 100000]);;

expected_orders := [1, 2, 4, 8, 16, 32, 64, 128];;
expected_counts := [1, 1, 2, 5, 14, 51, 267, 2328];;
smallgrp_info := PackageInfo("smallgrp");;

if Length(smallgrp_info) = 0 then
    Error("the GAP smallgrp package is unavailable");
fi;

Print("AMRA_KOU21137_CAYLEY_V2\n");
Print(
    "META|gap=", GAPInfo.Version,
    "|smallgrp=", smallgrp_info[1].Version, "\n"
);

total := 0;;
for order_index in [1 .. Length(expected_orders)] do
    order := expected_orders[order_index];;
    count := NumberSmallGroups(order);;
    if count <> expected_counts[order_index] then
        Error(
            "unexpected SmallGroups count at order ", order,
            ": expected ", expected_counts[order_index],
            ", got ", count
        );
    fi;
    Print("COUNT|", order, "|", count, "\n");

    for catalogue_id in [1 .. count] do
        group := SmallGroup(order, catalogue_id);;
        table := MultiplicationTable(group);;
        if Length(table) <> order then
            Error("wrong multiplication-table size");
        fi;

        table_bytes := "";;
        Print("BEGIN|", order, "|", catalogue_id, "|", order, "\n");
        for row_index in [1 .. order] do
            row := table[row_index];;
            if Length(row) <> order then
                Error("wrong multiplication-table row size");
            fi;
            Print("ROW|", row_index);
            for column_index in [1 .. order] do
                entry := row[column_index];;
                if entry < 1 or entry > order then
                    Error("multiplication-table entry out of range");
                fi;
                Add(table_bytes, CharInt(entry - 1));
                Print("|", entry);
            od;
            Print("\n");
        od;
        Print("TABLE_SHA256|", HexSHA256(table_bytes), "\n");
        Print("END|", order, "|", catalogue_id, "\n");
        total := total + 1;
    od;
od;

if total <> Sum(expected_counts) then
    Error("incomplete SmallGroups traversal");
fi;
Print("DONE|", total, "\n");
QUIT;
