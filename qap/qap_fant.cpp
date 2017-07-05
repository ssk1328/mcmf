#include <iostream>
#include <fstream>
#include <math.h>
#include <time.h>
const long n_max = 351;  // maximum size of the problem

/* Programme for approximately solving the quadratic assignment problem.
   Language : c++; compiler g++ should work.
   

   Method: FANT, Described in E. D. Taillard, 
   "FANT: Fast ant system",
   Technical report IDSIA-46-98, IDSIA, Lugano, 1998.

   Implementation : E. Taillard, 14. 10. 98
   Copyright :      E. Taillard, 14. 10. 98
   Available on :   http://www.eivd.ch/ina/collaborateurs/etd

   Data :
     size of the problem, parameter R, number of FANT iterations
     distance matrix   
     flow matrix

   Exemple of valid data 
  (for problem tai10b, to be included in a file, e. g. tai10b.dat) :

  10 6 50

 0   19  78  60 79  45  65  37 103  34
 19   0  65  45 76  63  79  22 109  19
 78  65   0  21 44 113 104  72  97  73
 60  45  21   0 53  99  97  50 102  51
 79  76  44  53  0  98  74  93  54  92
 45  63 113  99 98   0  42  81  97  78
 65  79 104  97 74  42   0 100  57  98
 37  22  72  50 93  81 100   0 130   3
103 109  97 102 54  97  57 130   0 128
 34  19  73  51 92  78  98   3 128   0

   0    1    0    2  0    0  15    0   0  172
 171    0    0   14  0   61  30    0 886   45
  43    0    0 2106  1    0   0    0   0    0
 361    0    0    0  0    0   0    0   0    0
   2  123    1    0  0   49  18    0 335 2417
1096    0    0    0  0    0 952    5   0    0
 207 3703   27    0  4    0   0    0 202    0
  16   58    0    0  0    0 546    0  42 1213
   0    0    0   53  0  546   7 2649   0   86
   0    0 6707    1 12 7124   1    0   1    0

Running with the data given above the programme gives :

Data file name : 
tai10b.dat
New best solution value, cost : 1217793 Found at iteration : 1
5 6 1 4 8 7 2 3 9 10 
New best solution value, cost : 1183760 Found at iteration : 6
5 6 1 4 7 8 9 3 2 10 

*/

const long infini = 1399999999;

typedef long  type_vecteur[n_max];
typedef long type_matrice[n_max][n_max];

/*--------------- choses manquantes -----------------*/
enum booleen {faux, vrai};

void swap(long &a, long &b) {long temp = a; a = b; b = temp;}

void a_la_ligne(ifstream & fichier_donnees)
{char poubelle[1000]; fichier_donnees.getline(poubelle, sizeof(poubelle));}
/*-------------------------------------------------*/


/************* random number generator, utility ****************/
const long m = 2147483647; const long m2 = 2145483479; 
const long a12 = 63308; const long q12 = 33921; const long r12 = 12979; 
const long a13 = -183326; const long q13 = 11714; const long r13 = 2883; 
const long a21 = 86098; const long q21 = 24919; const long r21 = 7417; 
const long a23 = -539608; const long q23 = 3976; const long r23 = 2071;
const double invm = 4.656612873077393e-10;

double rand(long & x10, long & x11, long & x12, 
            long & x20, long & x21, long & x22)
 {long h, p12, p13, p21, p23;
  h = x10/q13; p13 = -a13*(x10-h*q13)-h*r13;
  h = x11/q12; p12 = a12*(x11-h*q12)-h*r12;
  if (p13 < 0) p13 = p13 + m; if (p12 < 0) p12 = p12 + m;
  x10 = x11; x11 = x12; x12 = p12-p13; if (x12 < 0) x12 = x12 + m;
  h = x20/q23; p23 = -a23*(x20-h*q23)-h*r23;
  h = x22/q21; p21 = a21*(x22-h*q21)-h*r21;
  if (p23 < 0) p23 = p23 + m2; if (p21 < 0) p21 = p21 + m2;
  x20 = x21; x21 = x22; x22 = p21-p23; if(x22 < 0) x22 = x22 + m2;
  if (x12 < x22) h = x12 - x22 + m; else h = x12 - x22;
  if (h == 0) return(1.0); else return(h*invm);
 }

long germe1 = 12345, germe2 = 67890, germe3 = 13579, 
     germe4 = 24680, germe5 = 98765, germe6 = 43210;

long unif(long low, long high)
 {return(low + long(double(high - low + 1) * 
          rand(germe1, germe2, germe3, germe4, germe5, germe6)));
 }

/**********************************************************/

void lire(long & n, long & R, long & nb_iterations,  
          type_matrice & a, type_matrice & b)
// read problem data and parameters
 {ifstream fichier_donnees;
  char nom_fichier[30];
  long i, j;

  cout << "Data file name : \n";
  cin >> nom_fichier;
  fichier_donnees.open(nom_fichier);
  fichier_donnees >> n; a_la_ligne(fichier_donnees);
  cout << " parameter R and number of iterations : \n";
  cin >> R >> nb_iterations; 
  if (n >= n_max) 
    {cout << "Resize constant n_max to : " << n+1 
          << " at the beginning of the code \n";
/*     exit; not supported by some compiler */
    };
  for (i = 1; i <= n; i = i+1) for (j = 1; j <= n; j = j+1)
    fichier_donnees >> a[i][j];
  for (i = 1; i <= n; i = i+1) for (j = 1; j <= n; j = j+1)
    fichier_donnees >> b[i][j];
  fichier_donnees.close();
 }

void imprime(long n, type_vecteur p) 
// print solution p
 {long i; for (i = 1; i <= n; i = i + 1) cout << p[i] << ' '; cout << '\n';}
   
long calc_delta(long n, type_matrice & a, type_matrice & b,
                type_vecteur & p, long r, long s)
// compute the value of move (r, s) on solution p
 {long d; long k;
  d = (a[r][r]-a[s][s])*(b[p[s]][p[s]]-b[p[r]][p[r]]) +
      (a[r][s]-a[s][r])*(b[p[s]][p[r]]-b[p[r]][p[s]]);
  for (k = 1; k <= n; k = k + 1) if (k!=r && k!=s)
    d = d + (a[k][r]-a[k][s])*(b[p[k]][p[s]]-b[p[k]][p[r]]) +
            (a[r][k]-a[s][k])*(b[p[s]][p[k]]-b[p[r]][p[k]]);
  return(d);
 }

long calcule_cout(long n, type_matrice & a, type_matrice & b, type_vecteur & p)
// compute the cost of solution p
 {long c = 0; long i, j;
  for (i = 1; i <= n; i = i + 1) for (j = 1; j <= n; j = j + 1)
    c = c + a[i][j] * b[p[i]][p[j]];
  return(c);
 }

void tire_solution_aleatoire(long n, type_vecteur  & p)
// generate a random permutation p
 {long i;
  for (i = 0; i <= n; i = i+1) p[i] = i;
  for (i = 2; i <= n; i = i+1) swap(p[i-1], p[unif(i-1, n)]);
 }

void replace(long n, type_matrice & a, type_matrice & b,
             type_vecteur & p, long & Cout)
// local search
 {booleen a_tester[n_max][n_max];
  long r, s, i, ii, rr, ss, j;
  long delta;
  type_vecteur ps, pr;
  booleen ameliore = vrai;
  for (i = 1; i <= n; i = i + 1) for (j = 1; j <= n; j = j + 1)
    a_tester[i][j] = vrai;
  for (i = 1; i <= n; i = i + 1) a_tester[i][i] = faux;
  for (ii = 1; ii <= 2 && ameliore == vrai; ii = ii + 1)
   {ameliore = faux;
    tire_solution_aleatoire(n, pr);
    for (rr = 1; rr <= n; rr = rr + 1)
     {r = pr[rr];
      tire_solution_aleatoire(n, ps);
      for (ss = 1; ss <= n; ss = ss + 1)
       {s = ps[ss];
        if (a_tester[r][s] == vrai)
         {delta = calc_delta(n, a, b, p, r, s);
          if (delta < 0)
           {Cout = Cout + delta; swap(p[r], p[s]); ameliore = vrai;
            for (i = 1; i <= n; i = i + 1) 
              for (j = 1; j <= n; j = j + 1) a_tester[i][j] = vrai;
            for (i = 1; i <= n; i = i + 1) a_tester[i][i] = faux;
           };
          a_tester[r][s] = faux; a_tester[s][r] = faux;
         }; // a_tester
       }; // for ss
     };
   };
 }


/************************ memory management *************************/

void initialise_trace(long n, long increment, type_matrice & trace)
// (re-) initialization of the memory
 {long i, j;
  for (i = 1; i <= n; i = i+1) for (j = 1; j <= n; j = j+1)
    trace[i][j] = increment;
 }

void ajourne_trace(long n, type_vecteur & p, type_vecteur & m,
                   long increment, long R, type_matrice & trace)
// memory update
 {long i;
  for (i = 1; i <= n; i = i+1) trace[i][p[i]] = trace[i][p[i]] + increment;
  for (i = 1; i <= n; i = i+1) trace[i][m[i]] = trace[i][m[i]] + R;
 }

void tire_solution_trace(long n, type_vecteur & p, type_vecteur & m,
                         long & increment, type_matrice & trace)
// build a new solution probabilistically
 {long i, j, ii, k;
  booleen choisi[n_max];
  type_vecteur nb;
  for (i = 1; i <= n; i = i+1) nb[i] = 0;
  for (i = 1; i <= n; i = i+1) for (j = 1; j <= n; j = j+1)
    nb[i] = nb[i] + trace[i][j];
  for (i = 1; i <= n; i = i+1) choisi[i] = faux;
  long uu = unif(1, n);
  for (ii = 1; ii <= n; ii = ii+1)
   {long i = ((ii + uu) % n) + 1;
    long u = unif(1, nb[i]);
    long j = unif(1, n);
    while(choisi[j] == vrai) j = (j % n) + 1;
    long s = trace[i][j];
    while (s < u)
     {j = (j%n)+1;
      while(choisi[j] == vrai) j = (j % n) + 1;
      s = s + trace[i][j];
     };
    p[i] = j; choisi[j] = vrai;

    for (k = 1; k <= n; k = k+1) nb[k] = nb[k] - trace[k][j];
   };
  booleen identique = vrai;
  for (k = 1; k <= n && identique == vrai; k = k + 1)
    if (p[k] != m[k]) identique = faux;
  if (identique == vrai) 
   {increment = 1+increment; initialise_trace(n, increment, trace);};
 }
/********************************************************************/


long  n;                                 // size of the problem
long Cout, meilleur_cout;                // cost of current solution, best cost
type_matrice a, b;                       // flow and distance matrices
type_vecteur p, mp;                      // current solution and best solution
long nb_iterations;                      // number of FANT iterations
type_matrice memory;                     // memory
long increment, R;                       // parameter for managing the traces
long k, no_iteration;                    // iteration counters

main()
 {lire(n, R, nb_iterations, a, b);       // read problem data and parameter R
  if (n >= n_max) return(0);

                                         // initializations
  increment = 1;
  initialise_trace(n, increment, memory);
  meilleur_cout = infini;
                                         // FANT iterations
  for (no_iteration = 1; no_iteration <= nb_iterations;
       no_iteration = no_iteration + 1)
                                                   // Build a new solution
   {tire_solution_trace(n, p, mp, increment, memory);
    Cout = calcule_cout(n, a, b, p);
                                                   // Local search
    replace(n, a, b, p, Cout);
                                                   // Best solution improved ?
    if (Cout < meilleur_cout)
     {meilleur_cout = Cout; 
      cout << 
        "New best solution value, cost : " <<
        Cout << " Found at iteration : " << 
        no_iteration << '\n';
      for (k = 1; k <= n; k = k + 1) mp[k] = p[k];
      imprime(n, p);
      increment = 1;
      initialise_trace(n, increment, memory);
     };
                                                  // Memory update
    ajourne_trace(n, p, mp, increment, R, memory);
   };
 }
