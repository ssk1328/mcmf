import MemTypes::*;
import ProcTypes::*;

// Python generated code which returns arc_id for each pair of source and destination of packets 

function NoCArcId lookupNoCArcId(ProcID srcProcId, ProcID destProcID);
  NoCArcId arc_id = 0;

  if (srcProcId == 0) begin
    if (destProcID == 1) arc_id = 0;
    else if(destProcID == 3) arc_id = 1;
    else if(destProcID == 6) arc_id = 2;
    else if(destProcID == 4) arc_id = 3;
  end
  else if (srcProcId == 1) begin
    if (destProcID == 2) arc_id = 4;
    else if(destProcID == 4) arc_id = 5;
    else if(destProcID == 0) arc_id = 6;
    else if(destProcID == 5) arc_id = 7;
  end
  else if (srcProcId == 2) begin
    if (destProcID == 3) arc_id = 8;
    else if(destProcID == 5) arc_id = 9;
    else if(destProcID == 1) arc_id = 10;
    else if(destProcID == 6) arc_id = 11;
  end
  else if (srcProcId == 3) begin
    if (destProcID == 4) arc_id = 12;
    else if(destProcID == 6) arc_id = 13;
    else if(destProcID == 2) arc_id = 14;
    else if(destProcID == 0) arc_id = 15;
  end
  else if (srcProcId == 4) begin
    if (destProcID == 5) arc_id = 16;
    else if(destProcID == 0) arc_id = 17;
    else if(destProcID == 3) arc_id = 18;
    else if(destProcID == 1) arc_id = 19;
  end
  else if (srcProcId == 5) begin
    if (destProcID == 6) arc_id = 20;
    else if(destProcID == 1) arc_id = 21;
    else if(destProcID == 4) arc_id = 22;
    else if(destProcID == 2) arc_id = 23;
  end
  else if (srcProcId == 6) begin
    if (destProcID == 0) arc_id = 24;
    else if(destProcID == 2) arc_id = 25;
    else if(destProcID == 5) arc_id = 26;
    else if(destProcID == 3) arc_id = 27;
  end
  else arc_id 0;

return arc_id;

endfunction: lookupNoCArcId


// Lookup function for destination node at each mesh node corresponding to the arc id and source mesh 
function String lookupArcDest ( NoCAddr2D thisRowAddr, NoCAddr2D thisColAddr, NoCArcId arc_index); 
endfunction 
  if ((thisRowAddr == 2) & (thisColAddr == 0)) begin 
    if (arc_index == 0) return "N"  ;
    if (arc_index == 1) return "E"  ;
    if (arc_index == 2) return "E"  ;
    if (arc_index == 3) return "E"  ;
    if (arc_index == 6) return "H"  ;
    if (arc_index == 15) return "H"  ;
    if (arc_index == 17) return "H"  ;
    if (arc_index == 24) return "H"  ;
  end 
  if ((thisRowAddr == 1) & (thisColAddr == 0)) begin 
    if (arc_index == 0) return "H"  ;
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
    if (arc_index == 8) return "S"  ;
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
    if (arc_index == 3) return "N"  ;
    if (arc_index == 8) return "H"  ;
    if (arc_index == 12) return "N"  ;
    if (arc_index == 13) return "E"  ;
    if (arc_index == 14) return "E"  ;
    if (arc_index == 15) return "W"  ;
    if (arc_index == 18) return "H"  ;
    if (arc_index == 24) return "W"  ;
    if (arc_index == 27) return "H"  ;
  end 
  if ((thisRowAddr == 1) & (thisColAddr == 1)) begin 
    if (arc_index == 3) return "H"  ;
    if (arc_index == 5) return "H"  ;
    if (arc_index == 7) return "E"  ;
    if (arc_index == 12) return "H"  ;
    if (arc_index == 16) return "E"  ;
    if (arc_index == 17) return "W"  ;
    if (arc_index == 18) return "S"  ;
    if (arc_index == 19) return "W"  ;
    if (arc_index == 21) return "W"  ;
    if (arc_index == 22) return "H"  ;
  end 
  if ((thisRowAddr == 1) & (thisColAddr == 2)) begin 
    if (arc_index == 7) return "H"  ;
    if (arc_index == 8) return "S"  ;
    if (arc_index == 9) return "H"  ;
    if (arc_index == 11) return "S"  ;
    if (arc_index == 14) return "N"  ;
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
    if (arc_index == 8) return "W"  ;
    if (arc_index == 11) return "H"  ;
    if (arc_index == 13) return "H"  ;
    if (arc_index == 14) return "N"  ;
    if (arc_index == 20) return "H"  ;
    if (arc_index == 24) return "W"  ;
    if (arc_index == 25) return "N"  ;
    if (arc_index == 26) return "N"  ;
    if (arc_index == 27) return "W"  ;
  end 
  if ((thisRowAddr == 0) & (thisColAddr == 0)) begin 
    if (arc_index == 4) return "E"  ;
    if (arc_index == 10) return "S"  ;
  end 
  if ((thisRowAddr == 0) & (thisColAddr == 1)) begin 
    if (arc_index == 4) return "E"  ;
    if (arc_index == 10) return "W"  ;
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
