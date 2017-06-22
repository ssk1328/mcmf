import MemTypes::*;
import ProcTypes::*;

// Python generated code which returns arc_id for each pair of source and destination of packets 

function NoCArcId lookupNoCArcId(ProcID srcProcId, ProcID destProcID, PacketLocation packLoc);
  NoCArcId arc_id = 0;

  if (srcProcId == 0) begin
    if (destProcID == 1) begin 
      if ( packLoc < 8) arc_id = 0; 
    end

    else if(destProcID == 3) begin 
      if ( packLoc < 8) arc_id = 1; 
    end

    else if(destProcID == 4) begin 
      if ( packLoc < 8) arc_id = 3; 
    end

    else if(destProcID == 6) begin 
      if ( packLoc < 8) arc_id = 2; 
    end

  end

  else if (srcProcId == 1) begin
    if (destProcID == 0) begin 
      if ( packLoc < 8) arc_id = 6; 
    end

    else if(destProcID == 2) begin 
      if ( packLoc < 8) arc_id = 4; 
    end

    else if(destProcID == 4) begin 
      if ( packLoc < 8) arc_id = 5; 
    end

    else if(destProcID == 5) begin 
      if ( packLoc < 8) arc_id = 7; 
    end

  end

  else if (srcProcId == 2) begin
    if (destProcID == 1) begin 
      if ( packLoc < 8) arc_id = 10; 
    end

    else if(destProcID == 3) begin 
      if ( packLoc < 8) arc_id = 8; 
    end

    else if(destProcID == 5) begin 
      if ( packLoc < 8) arc_id = 9; 
    end

    else if(destProcID == 6) begin 
      if ( packLoc < 8) arc_id = 11; 
    end

  end

  else if (srcProcId == 3) begin
    if (destProcID == 0) begin 
      if ( packLoc < 8) arc_id = 15; 
    end

    else if(destProcID == 2) begin 
      if ( packLoc < 8) arc_id = 14; 
    end

    else if(destProcID == 4) begin 
      if ( packLoc < 8) arc_id = 12; 
    end

    else if(destProcID == 6) begin 
      if ( packLoc < 8) arc_id = 13; 
    end

  end

  else if (srcProcId == 4) begin
    if (destProcID == 0) begin 
      if ( packLoc < 8) arc_id = 17; 
    end

    else if(destProcID == 1) begin 
      if ( packLoc < 8) arc_id = 19; 
    end

    else if(destProcID == 3) begin 
      if ( packLoc < 8) arc_id = 18; 
    end

    else if(destProcID == 5) begin 
      if ( packLoc < 8) arc_id = 16; 
    end

  end

  else if (srcProcId == 5) begin
    if (destProcID == 1) begin 
      if ( packLoc < 8) arc_id = 21; 
    end

    else if(destProcID == 2) begin 
      if ( packLoc < 8) arc_id = 23; 
    end

    else if(destProcID == 4) begin 
      if ( packLoc < 8) arc_id = 22; 
    end

    else if(destProcID == 6) begin 
      if ( packLoc < 8) arc_id = 20; 
    end

  end

  else if (srcProcId == 6) begin
    if (destProcID == 0) begin 
      if ( packLoc < 8) arc_id = 24; 
    end

    else if(destProcID == 2) begin 
      if ( packLoc < 8) arc_id = 25; 
    end

    else if(destProcID == 3) begin 
      if ( packLoc < 8) arc_id = 27; 
    end

    else if(destProcID == 5) begin 
      if ( packLoc < 8) arc_id = 26; 
    end

  end

  return arc_id;

endfunction: lookupNoCArcId


// Lookup function for destination node at each mesh node corresponding to the arc id and source mesh 
function String lookupArcDest ( NoCAddr2D thisRowAddr, NoCAddr2D thisColAddr, NoCArcId arc_index); 
  String dest_direction = "N";
  if ((thisRowAddr == 2) && (thisColAddr == 0)) begin 
    if (arc_index == 0) dest_direction = "N"  ;
    if (arc_index == 1) dest_direction = "E"  ;
    if (arc_index == 2) dest_direction = "E"  ;
    if (arc_index == 3) dest_direction = "E"  ;
    if (arc_index == 6) dest_direction = "H"  ;
    if (arc_index == 15) dest_direction = "H"  ;
    if (arc_index == 17) dest_direction = "H"  ;
    if (arc_index == 24) dest_direction = "H"  ;
  end 
  if ((thisRowAddr == 1) && (thisColAddr == 0)) begin 
    if (arc_index == 0) dest_direction = "H"  ;
    if (arc_index == 4) dest_direction = "E"  ;
    if (arc_index == 5) dest_direction = "E"  ;
    if (arc_index == 6) dest_direction = "S"  ;
    if (arc_index == 7) dest_direction = "E"  ;
    if (arc_index == 10) dest_direction = "H"  ;
    if (arc_index == 17) dest_direction = "S"  ;
    if (arc_index == 19) dest_direction = "H"  ;
    if (arc_index == 21) dest_direction = "H"  ;
  end 
  if ((thisRowAddr == 0) && (thisColAddr == 2)) begin 
    if (arc_index == 4) dest_direction = "H"  ;
    if (arc_index == 8) dest_direction = "W"  ;
    if (arc_index == 9) dest_direction = "S"  ;
    if (arc_index == 10) dest_direction = "W"  ;
    if (arc_index == 11) dest_direction = "S"  ;
    if (arc_index == 14) dest_direction = "H"  ;
    if (arc_index == 23) dest_direction = "H"  ;
    if (arc_index == 25) dest_direction = "H"  ;
  end 
  if ((thisRowAddr == 2) && (thisColAddr == 1)) begin 
    if (arc_index == 1) dest_direction = "H"  ;
    if (arc_index == 2) dest_direction = "E"  ;
    if (arc_index == 3) dest_direction = "N"  ;
    if (arc_index == 8) dest_direction = "H"  ;
    if (arc_index == 12) dest_direction = "N"  ;
    if (arc_index == 13) dest_direction = "E"  ;
    if (arc_index == 14) dest_direction = "E"  ;
    if (arc_index == 15) dest_direction = "W"  ;
    if (arc_index == 18) dest_direction = "H"  ;
    if (arc_index == 24) dest_direction = "W"  ;
    if (arc_index == 27) dest_direction = "H"  ;
  end 
  if ((thisRowAddr == 1) && (thisColAddr == 1)) begin 
    if (arc_index == 3) dest_direction = "H"  ;
    if (arc_index == 4) dest_direction = "E"  ;
    if (arc_index == 5) dest_direction = "H"  ;
    if (arc_index == 7) dest_direction = "E"  ;
    if (arc_index == 8) dest_direction = "S"  ;
    if (arc_index == 12) dest_direction = "H"  ;
    if (arc_index == 16) dest_direction = "E"  ;
    if (arc_index == 17) dest_direction = "W"  ;
    if (arc_index == 18) dest_direction = "S"  ;
    if (arc_index == 19) dest_direction = "W"  ;
    if (arc_index == 21) dest_direction = "W"  ;
    if (arc_index == 22) dest_direction = "H"  ;
  end 
  if ((thisRowAddr == 1) && (thisColAddr == 2)) begin 
    if (arc_index == 4) dest_direction = "N"  ;
    if (arc_index == 7) dest_direction = "H"  ;
    if (arc_index == 9) dest_direction = "H"  ;
    if (arc_index == 11) dest_direction = "S"  ;
    if (arc_index == 14) dest_direction = "N"  ;
    if (arc_index == 16) dest_direction = "H"  ;
    if (arc_index == 20) dest_direction = "S"  ;
    if (arc_index == 21) dest_direction = "W"  ;
    if (arc_index == 22) dest_direction = "W"  ;
    if (arc_index == 23) dest_direction = "N"  ;
    if (arc_index == 25) dest_direction = "N"  ;
    if (arc_index == 26) dest_direction = "H"  ;
  end 
  if ((thisRowAddr == 2) && (thisColAddr == 2)) begin 
    if (arc_index == 2) dest_direction = "H"  ;
    if (arc_index == 11) dest_direction = "H"  ;
    if (arc_index == 13) dest_direction = "H"  ;
    if (arc_index == 14) dest_direction = "N"  ;
    if (arc_index == 20) dest_direction = "H"  ;
    if (arc_index == 24) dest_direction = "W"  ;
    if (arc_index == 25) dest_direction = "N"  ;
    if (arc_index == 26) dest_direction = "N"  ;
    if (arc_index == 27) dest_direction = "W"  ;
  end 
  if ((thisRowAddr == 0) && (thisColAddr == 0)) begin 
    if (arc_index == 10) dest_direction = "S"  ;
  end 
  if ((thisRowAddr == 0) && (thisColAddr == 1)) begin 
    if (arc_index == 8) dest_direction = "S"  ;
    if (arc_index == 10) dest_direction = "W"  ;
  end 
  return dest_direction;
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
