#!/bin/bash

echo node-r26.data.legion.ucl.ac.uk > nodes.old
echo node-r27.data.legion.ucl.ac.uk >> nodes.old

for a in `seq -w 1 28`
do
  echo node-s$a.data.legion.ucl.ac.uk >> nodes.old
done

for a in `seq -w 1 36`
do
  echo node-t$a.data.legion.ucl.ac.uk >> nodes.old
done

for a in `seq -w 1 22`
do
  echo node-u$a.data.legion.ucl.ac.uk >> nodes.old
done

echo node-u04a-026 > nodes.new
echo node-u04a-027 >> nodes.new

for a in `seq -w 1 28`
do
  echo node-u04a-0$a >> nodes.new
done

for a in `seq -w 1 36`
do
  echo node-u06a-0$a >> nodes.new
done

for a in `seq -w 1 22`
do
  echo node-u07a-0$a >> nodes.new
done