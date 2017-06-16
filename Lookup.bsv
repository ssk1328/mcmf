import MemTypes::*;
import ProcTypes::*;

// Python generated code which returns arc_id for each pair of source and destination of packets 

function NoCArcId lookupNoCArcId(ProcID srcProcId, ProcID destProcID);
  if (srcProcId == 0) begin
    if(destProcID == 1) return 0;
    if(destProcID == 3) return 1;
    if(destProcID == 6) return 2;
    if(destProcID == 4) return 3;
  end
  if (srcProcId == 1) begin
    if(destProcID == 2) return 4;
    if(destProcID == 4) return 5;
    if(destProcID == 0) return 6;
    if(destProcID == 5) return 7;
  end
  if (srcProcId == 2) begin
    if(destProcID == 3) return 8;
    if(destProcID == 5) return 9;
    if(destProcID == 1) return 10;
    if(destProcID == 6) return 11;
  end
  if (srcProcId == 3) begin
    if(destProcID == 4) return 12;
    if(destProcID == 6) return 13;
    if(destProcID == 2) return 14;
    if(destProcID == 0) return 15;
  end
  if (srcProcId == 4) begin
    if(destProcID == 5) return 16;
    if(destProcID == 0) return 17;
    if(destProcID == 3) return 18;
    if(destProcID == 1) return 19;
  end
  if (srcProcId == 5) begin
    if(destProcID == 6) return 20;
    if(destProcID == 1) return 21;
    if(destProcID == 4) return 22;
    if(destProcID == 2) return 23;
  end
  if (srcProcId == 6) begin
    if(destProcID == 0) return 24;
    if(destProcID == 2) return 25;
    if(destProcID == 5) return 26;
    if(destProcID == 3) return 27;
  end
  if (srcProcId == 7) begin
  end
  if (srcProcId == 8) begin
  end
  else return 0;
endfunction


// Lookup function for destination node at each mesh node corresponding to the arc id and source mesh 
function String lookupArcDest ( NoCAddr2D thisRowAddr, NoCAddr2D thisColAddr, NoCArcId arc_index); 
endfunction 
  if ((thisRowAddr == 2) & (thisColAddr == 0)) begin 
    if (arc_index == 0) return "N"  ;
    if (arc_index == 1) return "E"  ;
    if (arc_index == 2) return "E"  ;
    if (arc_index == 3) return "N"  ;
    if (arc_index == 6) return "H"  ;
    if (arc_index == 15) return "H"  ;
    if (arc_index == 17) return "H"  ;
    if (arc_index == 24) return "H"  ;
  end 
  if ((thisRowAddr == 1) & (thisColAddr == 0)) begin 
    if (arc_index == 0) return "H"  ;
    if (arc_index == 3) return "N"  ;
    if (arc_index == 4) return "N"  ;
    if (arc_index == 5) return "E"  ;
    if (arc_index == 6) return "S"  ;
    if (arc_index == 7) return "E"  ;
    if (arc_index == 10) return "H"  ;
    if (arc_index == 17) return "S"  ;
    if (arc_index == 19) return "H"  ;
    if (arc_index == 21) return "H"  ;
  end 
  if ((thisRowAddr == 0) & (thisColAddr == 2)) begin 
    if (arc_index == 4) return "H"  ;
    if (arc_index == 8) return "W"  ;
    if (arc_index == 9) return "S"  ;
    if (arc_index == 10) return "W"  ;
    if (arc_index == 11) return "S"  ;
    if (arc_index == 14) return "H"  ;
    if (arc_index == 23) return "H"  ;
    if (arc_index == 25) return "H"  ;
  end 
  if ((thisRowAddr == 2) & (thisColAddr == 1)) begin 
    if (arc_index == 1) return "H"  ;
    if (arc_index == 2) return "E"  ;
    if (arc_index == 8) return "H"  ;
    if (arc_index == 12) return "N"  ;
    if (arc_index == 13) return "E"  ;
    if (arc_index == 14) return "N"  ;
    if (arc_index == 15) return "W"  ;
    if (arc_index == 18) return "H"  ;
    if (arc_index == 24) return "W"  ;
    if (arc_index == 27) return "H"  ;
  end 
  if ((thisRowAddr == 1) & (thisColAddr == 1)) begin 
    if (arc_index == 3) return "H"  ;
    if (arc_index == 5) return "H"  ;
    if (arc_index == 7) return "E"  ;
    if (arc_index == 8) return "S"  ;
    if (arc_index == 12) return "H"  ;
    if (arc_index == 14) return "N"  ;
    if (arc_index == 16) return "E"  ;
    if (arc_index == 17) return "W"  ;
    if (arc_index == 18) return "S"  ;
    if (arc_index == 19) return "W"  ;
    if (arc_index == 21) return "N"  ;
    if (arc_index == 22) return "H"  ;
  end 
  if ((thisRowAddr == 1) & (thisColAddr == 2)) begin 
    if (arc_index == 7) return "H"  ;
    if (arc_index == 9) return "H"  ;
    if (arc_index == 11) return "S"  ;
    if (arc_index == 16) return "H"  ;
    if (arc_index == 20) return "S"  ;
    if (arc_index == 21) return "W"  ;
    if (arc_index == 22) return "W"  ;
    if (arc_index == 23) return "N"  ;
    if (arc_index == 25) return "N"  ;
    if (arc_index == 26) return "H"  ;
  end 
  if ((thisRowAddr == 2) & (thisColAddr == 2)) begin 
    if (arc_index == 2) return "H"  ;
    if (arc_index == 11) return "H"  ;
    if (arc_index == 13) return "H"  ;
    if (arc_index == 20) return "H"  ;
    if (arc_index == 24) return "W"  ;
    if (arc_index == 25) return "N"  ;
    if (arc_index == 26) return "N"  ;
    if (arc_index == 27) return "W"  ;
  end 
  if ((thisRowAddr == 0) & (thisColAddr == 0)) begin 
    if (arc_index == 3) return "E"  ;
    if (arc_index == 4) return "E"  ;
    if (arc_index == 10) return "S"  ;
    if (arc_index == 21) return "S"  ;
  end 
  if ((thisRowAddr == 0) & (thisColAddr == 1)) begin 
    if (arc_index == 3) return "S"  ;
    if (arc_index == 4) return "E"  ;
    if (arc_index == 8) return "S"  ;
    if (arc_index == 10) return "W"  ;
    if (arc_index == 14) return "E"  ;
    if (arc_index == 21) return "W"  ;
  end 
endfunction


// This is device placement generated from the qap solver used before hardcoded in mcmf.py file right now  
function MeshID lookupNoCAddr(ProcID currProcId); 
  case (currProcId)
    0: return 6; 
    1: return 3; 
    2: return 2; 
    3: return 7; 
    4: return 4; 
    5: return 5; 
    6: return 8; 
  endcase 
endfunction 
