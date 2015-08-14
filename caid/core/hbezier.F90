MODULE HBEZIER_POLAR
  IMPLICIT NONE

  REAL(KIND=8)      , PRIVATE :: pi= 4.0D0*ATAN(1.D0)
  INTEGER, PARAMETER, PRIVATE :: i_D0  = 1
  INTEGER, PARAMETER, PRIVATE :: i_DR  = 2
  INTEGER, PARAMETER, PRIVATE :: i_DZ  = 3
  INTEGER, PARAMETER, PRIVATE :: i_DRZ = 4 
  INTEGER, PARAMETER, PRIVATE :: i_DRR = 5 
  INTEGER, PARAMETER, PRIVATE :: i_DZZ = 6 

  INTEGER, PARAMETER, PRIVATE :: i_X_R = 1 
  INTEGER, PARAMETER, PRIVATE :: i_X_Z = 2 

  INTEGER, PARAMETER          :: N_DIM = 2 
  INTEGER, PARAMETER          :: POL_DIM = 2 
  INTEGER, PARAMETER          :: N_ORDER = 4 

CONTAINS

  ! -----------------------------------------------------------------------------
  ! -----------------------------------------------------------------------------
  SUBROUTINE construct_grid( &
                  & Rgeo, Zgeo, amin, acentre, angle_start, &
                  & nr, np,  &
                  & Coor2D, vertices, boundary, scales)
  IMPLICIT NONE
    ! --- Routine parameters
    ! Rgeo, Zgeo   : position of the geometric center
    ! amin, acentre: minor and smallest radius
    ! angle_start  : poloidal angle of first element
    ! Nr, Np       : number of radial&poloidal points
    REAL(KIND=8)                                                    , INTENT(IN)  :: Rgeo 
    REAL(KIND=8)                                                    , INTENT(IN)  :: Zgeo     
    REAL(KIND=8)                                                    , INTENT(IN)  :: amin
    REAL(KIND=8)                                                    , INTENT(IN)  :: acentre  
    REAL(KIND=8)                                                    , INTENT(IN)  :: angle_start    
    INTEGER(KIND=4)                                                 , INTENT(IN)  :: Nr
    INTEGER(KIND=4)                                                 , INTENT(IN)  :: Np        
    INTEGER(KIND=4), DIMENSION(4, (Nr-1)*Np)      , INTENT(OUT) :: vertices     
    INTEGER(KIND=4), DIMENSION(Nr*Np)                               , INTENT(OUT) :: boundary  
    REAL(KIND=8), DIMENSION(2, 4, Nr*Np)                  , INTENT(OUT) :: Coor2D          
    REAL(KIND=8), DIMENSION(4, 4, (Nr-1)*Np), INTENT(OUT) :: Scales   
    ! LOCAL
    INTEGER :: li_n_nodes
    INTEGER :: li_n_elmts
    INTEGER :: ir, ip, is, js, ks, ielmt, i, j
    INTEGER :: il, jl, id
    REAL(KIND=8)    :: Dr, dp, si, ti, Ray, theta, dr_ds, dtht_dt
    REAL(KIND=8), DIMENSION(2)    :: Xi, Xj, XR_r, SIG_r, XR_tht, SIG_tht
    REAL(KIND=8), DIMENSION(2)    :: Ui, Uj, Vj, Wj
    REAL(KIND=8), DIMENSION(3)    :: ABLTG
    REAL(KIND=8), DIMENSION(:), ALLOCATABLE :: S1, S2, SP1, SP2, SP3, SP4, RR    
    REAL(KIND=8), DIMENSION(:), ALLOCATABLE :: T1, T2, TP1, TP2, TP3, TP4, ZZ  

  ! -----------------------------------------------------------------------------
   ! -----------------------------------------------------------------------------

    li_n_nodes     = Nr*Np
    li_n_elmts     = (Nr-1)*Np

    Dr = 1.0/REAL(Nr-1)
    Dp = 2.d0*pi/REAL(Np) 

    ALLOCATE( RR(li_n_nodes), ZZ(li_n_nodes))
    ALLOCATE( S1(Nr), S2(Nr), SP1(Nr), SP2(Nr), SP3(Nr), SP4(Nr))
    ALLOCATE( T1(Np+1), T2(Np+1), TP1(Np+1), TP2(Np+1), TP3(Np+1), TP4(Np+1))

    T2 = 0.d0
    DO i=1,nr
       S1(i) = REAL(i-1)/REAL(nr-1)
    END DO

    DO j=1,np+1
       T1(j) = REAL(j-1)/REAL(np)
    END DO
    XR_r   = (/1.0, 0.10/)
    SIG_r  = (/1.0, 0.10/)

    XR_tht   = (/1.10, 0.10/)
    SIG_tht  = (/1.0, 0.10/)
!!$
!!$ XR_r(2)           !< Psi_N position of radial grid accumulation (two positions)
!!$ SIG_r(2)          !< Width of grid accumulation (two positions)
!!$ XR_tht(2)         !< Position of poloidal grid accumulation (0...1, two positions)
!!$ SIG_tht(2)        !< Width of grid accumulation (two positions)

    CALL meshac2(nr,S2,XR_r(1),XR_r(2),SIG_r(1),SIG_r(2),0.6d0,1.0d0)
    CALL spline(nr,S1,S2,0.d0,0.d0,2,SP1,SP2,SP3,SP4)

    CALL meshac2(np+1,T2,XR_tht(1),XR_tht(2),SIG_tht(1),SIG_tht(2),0.6d0,1.0d0)
    CALL spline(np+1,T1,T2,0.d0,0.d0,2,TP1,TP2,TP3,TP4)

    boundary = 0
    Loop_On_Radius : DO ir = 1, Nr
       si     = spwert(nr,S1(ir),SP1,SP2,SP3,SP4,S1,ABLTG)
       Ray    = ( acentre + (1.d0-acentre) * si )
       dr_ds  = (1.d0-acentre) * abltg(1)

       DO ip = 1, Np
          is    = isrp(ir,ip)

          theta    = angle_start + spwert(np+1,T1(ip),TP1,TP2,TP3,TP4,T1,ABLTG) * 2.d0 * PI
          dtht_dt  = abltg(1)

          Uj    = (/ COS(theta), SIN(theta) /)
          Vj    = (/-SIN(theta), COS(theta) /)
          Wj    = (/-SIN(theta), COS(theta) /)

          Coor2D(1:POL_DIM, i_D0,  is) = (/Rgeo, Zgeo/) &
               &          + Ray*(/ COS(theta), SIN(theta) /)
          Coor2D(1:POL_DIM, i_DR , is) = Uj       
          Coor2D(1:POL_DIM, i_DZ , is) = Vj    
          Coor2D(1:POL_DIM, i_DRZ, is) = Wj

          IF ( ir < Nr ) THEN
             ielmt = ielmtrp(ir,ip)
             IF( ip < Np) THEN
                js    = isrp(ir+1,ip)
                vertices(1:4 , ielmt) = (/is, js, js+1, is+1  /)
             ELSE
                js    = isrp(ir,1)
                vertices(1:4 , ielmt) = (/is, is+Np, js+Np, js  /)
             END IF
          END IF
          IF ( acentre < 0.00001 ) THEN 
             IF (ir .EQ. Nr) boundary(is) = 2 
          ELSE
             IF ((ir .EQ. 1) .OR. (ir .EQ. Nr)) boundary(is) = 2 
          END IF
       END DO
    END DO Loop_On_Radius
    ! -------------------------------------------------------------------------------------
    ! Scaling
    ! -------------------------------------------------------------------------------------
    DO ielmt = 1, li_n_elmts
       DO il = 1, 4
          id = MOD(il+1, 2) + 2
          jl = MOD(il, 4) + 1

          is = vertices(il, ielmt) 
          Xi = Coor2D(1:POL_DIM, i_D0 , is)
          Ui = Coor2D(1:POL_DIM, id   , is)

          js = vertices(jl, ielmt) 
          Xj = Coor2D(1:POL_DIM, i_D0 , js)
          Uj = Coor2D(1:POL_DIM, id   , js)

          Scales(id , il, ielmt) = SIGN(SQRT(SUM((Xj-Xi)**2)), SUM((Xj-Xi)*Ui) )/3.0
          Scales(id , jl, ielmt) = SIGN(SQRT(SUM((Xj-Xi)**2)), SUM((Xi-Xj)*Uj) )/3.0

       END DO

       DO il = 1, 4
          Scales(1 , il, ielmt)    =  1.0
          Scales(4 , il, ielmt)    =   &
               &  Scales(2 , il, ielmt) * Scales(3 , il, ielmt) 
       END DO

    END DO

    ! =========================================================================
  CONTAINS

    INTEGER FUNCTION isrp(irl, ipl)
      INTEGER :: irl, ipl
      isrp =  (irl-1)*Np + ipl
    END FUNCTION isrp

    INTEGER FUNCTION ielmtrp(irl, ipl)
      INTEGER :: irl, ipl
      ielmtrp =  (irl-1)*Np + ipl
    END FUNCTION ielmtrp

  END SUBROUTINE construct_grid

!************************************************************************
  REAL*8 FUNCTION SPWERT(N,XWERT,A,B,C,D,X,ABLTG)
    !-----------------------------------------------------------------------
    !     INPUT:
    !
    !     N           NUMBER OF GRID POINTS
    !     XWERT       STELLE AN DER FUNKTIONSWERTE BERECHNET WERDEN
    !    A, B, C, D  ARRAYS DER SPLINEKOEFFIZIENTEN (AUS SPLINE)
    !     X           ARRAY DER KNOTENPUNKTE
    !
    !     OUTPUT:
    !
    !     SPWERT   FUNKTIONSWERT AN DER STELLE XWERT
    !     ABLTG(I) I=1 : FIRST DERIVATIVE, ETC.
    !-----------------------------------------------------------------------

    IMPLICIT NONE
    INTEGER  N
    REAL(KIND=8)   XWERT, A(N), B(N), C(N), D(N), X(N), ABLTG(3), XX
    INTEGER  I, K, M

    !     SUCHE PASSENDES INTERVALL (BINAERE SUCHE)

    I = 1
    K = N

    DO 
       M = (I+K) / 2

       IF(M.NE.I) THEN
          IF(XWERT.LT.X(M)) THEN
             K = M
          ELSE
             I = M
          ENDIF
          CYCLE
       ENDIF
       EXIT
    END DO

    XX = XWERT - X(I)

    ABLTG(1) = (3.0d0 * D(I) * XX + 2.0d0 * C(I)) * XX + B(I)
    ABLTG(2) = 6.0d0 * D(I) * XX + 2.0d0 * C(I)
    ABLTG(3) = 6.0d0 * D(I)

    SPWERT = ((D(I)*XX + C(I))*XX + B(I))*XX + A(I)

  END FUNCTION SPWERT
  ! -----------------------------------------------------------------------------
  SUBROUTINE MESHAC2(NR,SG,XR1,XR2,SIG1,SIG2,BGF,FACT)
    !-----------------------------------------------------------------------
    ! subroutine to construct non-equidistant radial mesh
    ! the starting value is given by SG(1)
    !-----------------------------------------------------------------------
    INTEGER                    , INTENT(IN)    :: NR
    REAL(KIND=8), DIMENSION(:), INTENT(INOUT) :: SG
    REAL(KIND=8)                              :: XR1, XR2, SIG1, SIG2, BGF, FACT


    INTEGER, PARAMETER:: NMAX = 10001
    INTEGER :: I, J
    REAL(KIND=8)                       :: XSum, FINT2, FINT1, DSI, DFG, FI
    REAL(KIND=8), DIMENSION(NMAX)      :: S1, FXSum


    IF (NR .le. 0) RETURN    ! do nothing for zero points
    IF ((SG(1) .LT. 0.d0) .OR. (SG(1) .GE. 1.d0)) SG(1) = 0.d0

    !--------------------------------------- integrate gaussian
    DSI       = (1.d0 - SG(1)) / FLOAT(NMAX-1)
    S1(1)     = SG(1)
    FXSum(1)  = 0.d0
    XSum      = 0.d0
    FINT2     = FGAUS(S1(1),BGF,XR1,XR2,SIG1,SIG2,FACT,DFG)

!    WRITE(6,*) "DSI =",DSI, FINT2
    DO I = 2,NMAX
       S1(I)    = SG(1) + FLOAT(I-1) * DSI
       FINT1    = FINT2
       FINT2    = FGAUS(S1(I),BGF,XR1,XR2,SIG1,SIG2,FACT,DFG)
       XSum     = XSum + (FINT1+FINT2)/2.d0 * DSI
       FXSum(I) = XSum
    END DO

!    WRITE(6,*) "FXSum(NMAX) =",FXSum(NMAX)
    DO I=1,NMAX-1
       FXSum(I) = FXSum(I)/FXSum(NMAX)
    END DO

    FXSum(NMAX) = 1.d0

    J = 2
    DO I=2,NR-1
       FI = FLOAT(I-1)/FLOAT(NR-1)
       DO WHILE ((FI .gt. FXSum(J)) .and. (J .lt. NMAX))
          J = J + 1
       END DO
       SG(I)   = S1(J-1) + (FI-FXSum(J-1))/(FXSum(J)-FXSum(J-1))*(S1(J)-S1(J-1))
    END DO
    SG(NR)   = 1.d0
    SG(1)    = 0.d0
  END SUBROUTINE MESHAC2
  ! -----------------------------------------------------------------------------
  FUNCTION FGAUS(ZS,BGF,XR1,XR2,SIG1,SIG2,FACT,DFGAUSS)
    !-----------------------------------------------------------------------
    !     BGF + (1 - BGF) * (GAUSS1 + FACT * GAUSS2) / FACT
    !-----------------------------------------------------------------------
    IMPLICIT NONE
     REAL(KIND=8) :: ZS, BGF, XR1, XR2, SIG1, SIG2, FACT, DFGAUSS
     REAL(KIND=8) :: ZNORM1, ZNORM2, ZEX1, ZEX2, DEX1, DEX2, F1, F2, DF1, DF2
     REAL(KIND=8) :: FGAUS

    ZNORM1 = 0.39894d0 / SIG1
    ZNORM2 = 0.39894d0 / SIG2
    ZEX1   = -0.5d0 * (ZS - XR1)**2 / SIG1**2
    ZEX2   = -0.5d0 * (ZS - XR2)**2 / SIG2**2
    DEX1   = -(ZS-XR1)/SIG1**2
    DEX2   = -(ZS-XR2)/SIG2**2

    F1     = ZNORM1 * EXP(ZEX1)
    F2     = ZNORM2 * EXP(ZEX2)
    DF1    = ZNORM1 * DEX1 * EXP(ZEX1)
    DF2    = ZNORM2 * DEX2 * EXP(ZEX2)

    FGAUS   = BGF + (1.d0 - BGF) * (F1 + FACT * F2) / FACT
    DFGAUSS = (1.d0-BGF) * (DF1 + FACT * DF2) / FACT

  END FUNCTION FGAUS



!***********************************************************************
!    Routines from Jorek
!***********************************************************************
      SUBROUTINE SPLINE(N,X,Y,ALFA,BETA,TYP,A,B,C,D)
!-----------------------------------------------------------------------
!     INPUT:
!
!     N     NUMBER OF POINTS
!     X     ARRAY X VECTOR
!     Y     ARRAY Y VECTOR
!     ALFA  BOUNDARY CONDITION IN X(1)
!     BETA        "       IN X(N)
!     TYP   =  0  NOT-A-KNOT SPLINE
!              1  ALFA, BETA 1. ABLEITUNGEN VORGEGEBEN
!              2    "    "   2.     "           "
!              3    "    "   3.     "           "
!
!     BEME8UNG: MIT TYP = 2 UND ALFA = BETA = 0 ERHAELT MAN
!           EINEN NATUERLICHEN SPLINE
!
!     OUTPUT:
!
!     A, B, C, D     ARRAYS OF SPLINE COEFFICIENTS
!       S = A(I) + B(I)*(X-X(I)) + C(I)*(X-X(I))**2+ D(I)*(X-X(I))**3
!
!     BEI ANWENDUNGSFEHLERN WIRD DAS PROGRAMM MIT ENTSPRECHENDER
!     FEHLERMELDUNG ABGEBROCHEN
!-----------------------------------------------------------------------
!
!
      IMPLICIT NONE

      INTEGER  N, TYP
      REAL(KIND=8)    X(N), Y(N), ALFA, BETA, A(N), B(N), C(N), D(N)
      INTEGER  I, IERR
      REAL(KIND=8)    H(N)

      IF((TYP.LT.0).OR.(TYP.GT.3)) THEN
         WRITE(*,*) 'ERROR IN ROUTINE SPLINE: FALSE TYP'
         STOP
      ENDIF

      IF (N.LT.3) THEN
         WRITE(*,*) 'ERROR IN ROUTINE  SPLINE: N < 3'
         STOP
      ENDIF


!     BERECHNE DIFFERENZ AUFEINENDERFOLGENDER X-WERTE UND
!     UNTERSUCHE MONOTONIE
!
      DO I = 1, N-1
         H(I) = X(I+1)- X(I)
         IF(H(I).LE.0.d0) THEN
            WRITE(*,*) 'NON MONOTONIC ABCISSAE IN SPLINE: X(I-1)>=X(I)'
            STOP
         ENDIF
      ENDDO
!
!     AUFSTELLEN DES GLEICHUNGSSYSTEMS
!
      DO 20 I = 1, N-2
         A(I) = 3.d0 * ((Y(I+2)-Y(I+1)) / H(I+1) - (Y(I+1)-Y(I)) / H(I))
         B(I) = H(I)
         C(I) = H(I+1)
         D(I) = 2.d0 * (H(I) + H(I+1))
   20 CONTINUE
!
!     BERUECKSICHTIGEN DER RANDBEDINGUNGEN

!     NOT-A-KNOT

      IF(TYP.EQ.0) THEN
         A(1)   = A(1) * H(2) / (H(1) + H(2))
         A(N-2) = A(N-2) * H(N-2) / (H(N-1) + H(N-2))
         D(1)   = D(1) - H(1)
         D(N-2) = D(N-2) - H(N-1)
         C(1)   = C(1) - H(1)
         B(N-2) = B(N-2) - H(N-1)
      ENDIF

!     1. ABLEITUNG VORGEGEBEN

      IF(TYP.EQ.1) THEN
         A(1)   = A(1) - 1.5d0 * ((Y(2)-Y(1)) / H(1) - ALFA)
         A(N-2) = A(N-2) - 1.5d0 * (BETA - (Y(N)-Y(N-1)) / H(N-1))
         D(1)   = D(1) - 0.5d0 * H(1)
         D(N-2) = D(N-2) - 0.5d0 * H(N-1)
      ENDIF
!
!     2. ABLEITUNG VORGEGEBEN
!
      IF(TYP.EQ.2) THEN
         A(1)   = A(1) - 0.5d0 * ALFA * H(1)
         A(N-2) = A(N-2) - 0.5d0 * BETA * H(N-1)
      ENDIF

!     3. ABLEITUNG VORGEGEBEN
!
      IF(TYP.EQ.3 ) THEN
         A(1)   = A(1) + 0.5d0 * ALFA * H(1) * H(1)
         A(N-2) = A(N-2) - 0.5d0 * BETA * H(N-1)* H(N-1)
         D(1)   = D(1) + H(1)
         D(N-2) = D(N-2) + H(N-1)
      ENDIF

!     BERECHNUNG DER KOEFFIZIENTEN
!
      CALL DGTSL(N-2,B,D,C,A,IERR)
      IF(IERR.NE.0) THEN
         WRITE(*,21)
         STOP
      ENDIF

!     UEBERSCHREIBEN DES LOESUNGSVEKTORS

      CALL DCOPY(N-2,A,1,C(2),1)
!
!     IN ABHAENGIGKEIT VON DEN RANDBEDINGUNGEN WIRD DER 1. UND
!     DER LETZTE WERT VON C KORRIGIERT
!
      IF(TYP.EQ.0) THEN
         C(1) = C(2) + H(1) * (C(2)-C(3)) / H(2)
         C(N) = C(N-1) + H(N-1) * (C(N-1)-C(N-2)) / H(N-2)
      ENDIF

      IF(TYP.EQ.1) THEN
         C(1) = 1.5d0*((Y(2)-Y(1)) / H(1) - ALFA) / H(1) - 0.5d0 * C(2)
         C(N) = -1.5d0*((Y(N)-Y(N-1)) / H(N-1)-BETA) / H(N-1) - 0.5d0*C(N-1)
      ENDIF

      IF(TYP.EQ.2) THEN
         C(1) = 0.5d0 * ALFA
         C(N) = 0.5d0 * BETA
      ENDIF

      IF(TYP.EQ.3) THEN
         C(1) = C(2) - 0.5d0 * ALFA * H(1)
         C(N) = C(N-1) + 0.5d0 * BETA * H(N-1)
      ENDIF

      CALL DCOPY(N,Y,1,A,1)

      DO I = 1, N-1
         B(I) = (A(I+1)-A(I)) / H(I) - H(I) * (C(I+1)+2.0d0 * C(I)) / 3.0d0
         D(I) = (C(I+1)-C(I)) / (3.0d0 * H(I))
      END DO

      B(N) = (3.0d0 * D(N-1) * H(N-1) + 2.0d0 * C(N-1)) * H(N-1) + B(N-1)

      RETURN

   21 FORMAT(1X,'ERROR IN SGTSL: MATRIX SINGULAR')
      END  SUBROUTINE SPLINE 


!DECK DGTSL                                                             CAS02750
!** FROM NETLIB, TUE AUG 28 08:28:34 EDT 1990 ***
!** COPIED FROM SGTSL AND RENAMED             ***
!
      SUBROUTINE DGTSL(N,C,D,E,B,INFO)
      IMPLICIT NONE
      INTEGER N,INFO
      REAL(KIND=8)  C(*),D(*),E(*),B(*)

!     SGTSL GIVEN A GENERAL TRIDIAGONAL MATRIX AND A RIGHT HAND
!     SIDE WILL FIND THE SOLUTION.
!
!     ON ENTRY
!
!        N       INTEGER
!                IS THE ORDER OF THE TRIDIAGONAL MATRIX.
!
!
!        C       REAL(N)
!                IS THE SUBDIAGONAL OF THE TRIDIAGONAL MATRIX.
!                C(2) THROUGH C(N) SHOULD CONTAIN THE SUBDIAGONAL.
!                ON OUTPUT C IS DESTROYED.
!
!        D       REAL(N)
!                IS THE DIAGONAL OF THE TRIDIAGONAL MATRIX.
!                ON OUTPUT D IS DESTROYED.
!
!        E       REAL(N)
!                IS THE SUPERDIAGONAL OF THE TRIDIAGONAL MATRIX.
!                E(1) THROUGH E(N-1) SHOULD CONTAIN THE SUPERDIAGONAL.
!                ON OUTPUT E IS DESTROYED.
!
!        B       REAL(N)
!                IS THE RIGHT HAND SIDE VECTOR.
!
!     ON RETURN
!
!        B       IS THE SOLUTION VECTOR.
!
!        INFO    INTEGER
!                = 0 NORMAL VALUE.
!                = K IF THE K-TH ELEMENT OF THE DIAGONAL BECOMES
!                    EXACTLY ZERO.  THE SUBROUTINE RETURNS WHEN
!                    THIS IS DETECTED.
!
!     LINPACK. THIS VERSION DATED 08/14/78 .
!     JACK DONGARRA, ARGONNE NATIONAL LABORATORY.
!
!     NO EXTERNALS
!     FORTRAN ABS
!
!     INTERNAL VARIABLES
!
      INTEGER K,KB,KP1,NM1,NM2
      REAL(KIND=8) T
!     BEGIN BLOCK PERMITTING ...EXITS TO 100

         INFO = 0
         C(1) = D(1)
         NM1 = N - 1
         IF (NM1 .LT. 1) GO TO 40
            D(1) = E(1)
            E(1) = 0.0D0
            E(N) = 0.0D0

            DO 30 K = 1, NM1
               KP1 = K + 1

!              FIND THE LARGEST OF THE TWO ROWS

               IF (ABS(C(KP1)) .LT. ABS(C(K))) GO TO 10

!                 INTERCHANGE ROW

                  T = C(KP1)
                  C(KP1) = C(K)
                  C(K) = T
                  T = D(KP1)
                  D(KP1) = D(K)
                  D(K) = T
                  T = E(KP1)
                  E(KP1) = E(K)
                  E(K) = T
                  T = B(KP1)
                  B(KP1) = B(K)
                  B(K) = T
   10          CONTINUE

!              ZERO ELEMENTS

               IF (C(K) .NE. 0.0D0) GO TO 20
                  INFO = K
!     ............EXIT
                  GO TO 100
   20          CONTINUE
               T = -C(KP1)/C(K)
               C(KP1) = D(KP1) + T*D(K)
               D(KP1) = E(KP1) + T*E(K)
               E(KP1) = 0.0D0
               B(KP1) = B(KP1) + T*B(K)
   30       CONTINUE
   40    CONTINUE
         IF (C(N) .NE. 0.0D0) GO TO 50
            INFO = N
         GO TO 90
   50    CONTINUE

!           BACK SOLVE

            NM2 = N - 2
            B(N) = B(N)/C(N)
            IF (N .EQ. 1) GO TO 80
               B(NM1) = (B(NM1) - D(NM1)*B(N))/C(NM1)
               IF (NM2 .LT. 1) GO TO 70
               DO 60 KB = 1, NM2
                  K = NM2 - KB + 1
                  B(K) = (B(K) - D(K)*B(K+1) - E(K)*B(K+2))/C(K)
   60          CONTINUE
   70          CONTINUE
   80       CONTINUE
   90    CONTINUE
  100 CONTINUE

      RETURN
      END SUBROUTINE DGTSL 

!!$
      SUBROUTINE  dcopy(n,dx,incx,dy,incy)
! 
!      copies a vector, x, to a vector, y.
!      uses unrolled loops for increments equal to one.
!      jack dongarra, linpack, 3/11/78.
!      modified 12/3/93, array(1) declarations changed to array(*)
! 
      REAL(KIND=8)   :: dx(*),dy(*)
      INTEGER i,incx,incy,ix,iy,m,mp1,n
! 
      IF(n<=0)RETURN
      IF(incx==1 .AND. incy==1)go to 20
! 
!         code for unequal increments or equal increments
!           not equal to 1
! 
      ix = 1
      iy = 1
      IF(incx<0)ix = (-n+1)*incx + 1
      IF(incy<0)iy = (-n+1)*incy + 1
      DO 10 i = 1,n
        dy(iy) = dx(ix)
        ix = ix + incx
        iy = iy + incy
   10 CONTINUE
      RETURN
! 
!         code for both increments equal to 1
! 
! 
!         clean-up loop
! 
   20 m = MOD(n,7)
      IF( m == 0 ) go to 40
      DO 30 i = 1,m
        dy(i) = dx(i)
   30 CONTINUE
      IF( n < 7 ) RETURN
   40 mp1 = m + 1
      DO 50 i = mp1,n,7
        dy(i) = dx(i)
        dy(i + 1) = dx(i + 1)
        dy(i + 2) = dx(i + 2)
        dy(i + 3) = dx(i + 3)
        dy(i + 4) = dx(i + 4)
        dy(i + 5) = dx(i + 5)
        dy(i + 6) = dx(i + 6)
   50 CONTINUE
      RETURN
      END SUBROUTINE  dcopy 

END MODULE HBEZIER_POLAR




MODULE HBEZIER_SQUARE
  IMPLICIT NONE

  INTEGER, PARAMETER, PRIVATE :: i_D0  = 1
  INTEGER, PARAMETER, PRIVATE :: i_DR  = 2
  INTEGER, PARAMETER, PRIVATE :: i_DZ  = 3
  INTEGER, PARAMETER, PRIVATE :: i_DRZ = 4 
  INTEGER, PARAMETER, PRIVATE :: i_DRR = 5 
  INTEGER, PARAMETER, PRIVATE :: i_DZZ = 6 

  INTEGER, PARAMETER, PRIVATE :: i_X_R = 1 
  INTEGER, PARAMETER, PRIVATE :: i_X_Z = 2 

  INTEGER, PARAMETER          :: N_DIM = 2 
  INTEGER, PARAMETER          :: POL_DIM = 2 
  INTEGER, PARAMETER          :: N_ORDER = 4 

CONTAINS
  ! -----------------------------------------------------------------------------
  ! -----------------------------------------------------------------------------
  SUBROUTINE construct_grid( &
                  & Lx, Ly, Xmin, Ymin, &
                  & nr, np,  &
                  & Coor2D, vertices, boundary, scales)
    ! -------------------------------------------------------
    REAL(KIND=8)                                                    , INTENT(IN)  :: Lx
    REAL(KIND=8)                                                    , INTENT(IN)  :: Ly     
    REAL(KIND=8)                                                    , INTENT(IN)  :: Xmin
    REAL(KIND=8)                                                    , INTENT(IN)  :: Ymin
    INTEGER(KIND=4)                                                 , INTENT(IN)  :: Nr
    INTEGER(KIND=4)                                                 , INTENT(IN)  :: Np        
    INTEGER(KIND=4), DIMENSION(4, (Nr-1)*(Np-1))      , INTENT(OUT) :: vertices     
    INTEGER(KIND=4), DIMENSION(Nr*Np)                               , INTENT(OUT) :: boundary  
    REAL(KIND=8), DIMENSION(2, 4, Nr*Np)                  , INTENT(OUT) :: Coor2D          
    REAL(KIND=8), DIMENSION(4, 4, (Nr-1)*(Np-1)), INTENT(OUT) :: Scales   
    ! -------------------------------------------------------
    !       Local variables
    ! -------------------------------------------------------
    INTEGER :: li_n_nodes
    INTEGER :: li_n_elmts
    INTEGER          :: ir, ip, is, js, ks, ielmt
    INTEGER          :: il, jl, id
    REAL(KIND=8)    :: Dr, dp,  xxi, yyi
    REAL(KIND=8), DIMENSION(2)      :: Xi, Xj
    REAL(KIND=8), DIMENSION(2)      :: Ui, Uj, Vj, Wj
    ! -------------------------------------------------------
    ! -------------------------------------------------------

    li_n_nodes     = Nr*Np
    li_n_elmts     = (Nr-1)*(Np-1)

    Dr = Lx/REAL(Nr-1)
    Dp = Ly/REAL(Np-1) 

    boundary = 0     

    DO ir = 1, Nr
       xxi = Xmin + (ir-1)*Dr
       DO ip = 1, Np
          yyi  = Ymin + (ip-1)*Dp

          Uj    = (/ 1.0, 0.0 /)
          Vj    = (/ 0.0, 1.0 /)
          Wj    =  0.0
          is    = isrp(ir,ip)
          Coor2D(1:2, i_D0 , is) =  xxi*Uj(1:2)  + yyi*Vj(1:2)
          Coor2D(1:2, i_DR , is) = Uj(1:2)
          Coor2D(1:2, i_DZ , is) = Vj(1:2)
          Coor2D(1:2, i_DRZ, is) = Wj(1:2)

          IF ( ir < Nr ) THEN
             IF( ip < Np) THEN
                ielmt = ielmtrp(ir,ip)
                js    = isrp(ir+1,ip)
                vertices(1:4 , ielmt) = (/is, js, js+1, is+1  /)
              END IF

          END IF

          IF ((ir .EQ. 1) .OR. (ir .EQ. Nr)) boundary(is) = boundary(is) + 2
          IF ((ip .EQ. 1) .OR. (ip .EQ. Np)) boundary(is) = boundary(is) + 1
       END DO
    END DO
    ! Scaling
    DO ielmt = 1, li_n_elmts
       DO il = 1, 4 
          id = MOD(il+1, 2) + 2

          is = vertices(il, ielmt) 
          Xi = Coor2D(1:2, i_D0 , is)
          Ui = Coor2D(1:2, id   ,is)

          jl = MOD(il, 4) + 1
          js = vertices(jl, ielmt) 
          Xj = Coor2D(1:2, i_D0 , js)
          Uj = Coor2D(1:2, id   , js)    

          Scales(id , il, ielmt) =  1.0*SIGN( SQRT(SUM((Xi-Xj)**2)), SUM((Xj-Xi)*Ui) )/3
          Scales(id , jl, ielmt) =  1.0*SIGN( SQRT(SUM((Xi-Xj)**2)), SUM((Xi-Xj)*Uj) )/3
       END DO

       DO il = 1, 4
          Scales(1 , il, ielmt)    =  1.0
          Scales(4 , il, ielmt)    =   &
               &  Scales(2 , il, ielmt)*Scales(3 , il, ielmt) 
       END DO

    END DO

    ! =========================================================================
  CONTAINS

    INTEGER FUNCTION isrp(irl, ipl)
      INTEGER :: irl, ipl
      isrp =  (irl-1)*Np + ipl
    END FUNCTION isrp

    INTEGER FUNCTION ielmtrp(irl, ipl)
      INTEGER :: irl, ipl
      ielmtrp =  (irl-1)*(Np-1) + ipl
    END FUNCTION ielmtrp

  END SUBROUTINE construct_grid 

END MODULE HBEZIER_SQUARE

