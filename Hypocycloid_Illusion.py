import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation as ani


def HypocycloidCurve(Radius=1, IntRadius=.5, AngVelocity=2, IniExtAng=0, IniIntAng=0, ShowTrajectories=True):
    """
    Displays trajectories of a fixed point on a small circle rolling within another circle.

    Parameters
    ------------
    - Radius: Radius of the fixed circle.
    - IntRadius: Radius of the rolling circle.
    - AngVelocity: Angular velocity of the rolling circle.
    - IniExtAng: Initial exterior angle (between both circles' centers).
    - IniIntAng: Initial interior angle (between fixed point and rolling circle's center).
    - ShowTrajectories: Boolean, displays trajectories of both the fixed point and the center of the rolling circle.
    """
    try:
        CenterPosition = [[(Radius - IntRadius)*np.cos(IniExtAng)],
                          [(Radius - IntRadius)*np.sin(IniExtAng)]]
        MaxTime = 2*np.pi
        StepNumb = 320
        TimeDiscr = np.linspace(0, MaxTime, StepNumb)

        DotPosition = [[CenterPosition[0][0] + IntRadius *
                        np.cos(IniIntAng)], [CenterPosition[1][0] + IntRadius*np.sin(IniIntAng)]]

        for timestep in np.delete(TimeDiscr, 0):
            NewExtAngle = IniExtAng + AngVelocity*timestep
            NewCenterPos = [(Radius - IntRadius)*np.cos(NewExtAngle),
                            (Radius - IntRadius)*np.sin(NewExtAngle)]
            NewIntAngle = IniIntAng - AngVelocity * \
                timestep*(Radius-IntRadius)/IntRadius
            CenterPosition[0].append(NewCenterPos[0])
            CenterPosition[1].append(NewCenterPos[1])
            DotPosition[0].append(
                NewCenterPos[0]+IntRadius*np.cos(NewIntAngle))
            DotPosition[1].append(
                NewCenterPos[1]+IntRadius*np.sin(NewIntAngle))

        fig = plt.figure()
        ax = plt.axes(xlim=(-Radius-1, Radius+1), ylim=(-Radius-1, Radius+1))
        plt.suptitle("Hypocycloid Movement")
        DotPos, = ax.plot([], [], 'bo', lw=2)
        CenterPos, = ax.plot([], [], 'ro', lw=2)
        plt.plot([Radius*np.cos(t) for t in TimeDiscr],
                 [Radius*np.sin(t) for t in TimeDiscr])
        if ShowTrajectories:
            plt.plot(CenterPosition[0], CenterPosition[1], 'black', lw=.5)
            plt.plot(DotPosition[0], DotPosition[1], 'black', lw=.5)

        def animate(i):
            DotPos.set_data([DotPosition[0][i]], [DotPosition[1][i]])
            CenterPos.set_data([CenterPosition[0][i]], [CenterPosition[1][i]])
            return DotPos, CenterPos,

        anim = ani.FuncAnimation(fig, animate, init_func=None,
                                 frames=StepNumb, interval=20, blit=True)

        plt.axis('equal')
        plt.show()
    except:
        raise ValueError("Check arguments.")


def HypocycloidIllusion(DotNumber=1, ShowTrajectories=True, AngVelocity=2, ShowCircCenter=True):
    """
    Linear movement leads to circular movement illusion.

    Parameters
    ------------
    -DotNumber: Number of particles portraying linear movement (following a hypocycloid curve).
    -ShowTrajectories: Boolean, if True trajectories of each individual particle is shown.
    -AngVelocity: Velocity of movement of each particle depicting following a hypocyloid curve.
    -ShowCircCenter: Boolean, if true it depicts the mean position of all particles.
    """
    try:
        if (type(DotNumber) == int) and (DotNumber > 0):
            Radius = 1
            IntRadius = Radius/2
            Angle = 2*np.pi/DotNumber

            CenterList = []

            for cont in range(DotNumber):
                EachCenter = [(Radius - IntRadius)*np.cos(cont*Angle),
                              (Radius - IntRadius)*np.sin(cont*Angle)]
                CenterList.append(EachCenter)

            MaxTime = 2*np.pi
            StepNumb = 320
            TimeDiscr = np.linspace(0, MaxTime, StepNumb)

            DotsPositionList = []

            for cont in range(DotNumber):
                EachDotPosition = [[CenterList[cont][0]+IntRadius * np.cos(cont*Angle + (DotNumber-cont)*Angle)], [
                    CenterList[cont][1]+IntRadius * np.sin(cont*Angle + (DotNumber-cont)*Angle)]]
                DotsPositionList.append(EachDotPosition)

            for cont in range(DotNumber):
                for timestep in np.delete(TimeDiscr, 0):
                    NewExtAngle = cont*Angle + AngVelocity*timestep
                    EachNewPositionCenter = [
                        (Radius - IntRadius)*np.cos(NewExtAngle), (Radius - IntRadius)*np.sin(NewExtAngle)]
                    EachNewIntAngle = cont*Angle + \
                        (DotNumber-cont)*Angle - AngVelocity * \
                        timestep*(Radius)/Radius
                    DotsPositionList[cont][0].append(
                        EachNewPositionCenter[0] + IntRadius*np.cos(EachNewIntAngle))
                    DotsPositionList[cont][1].append(
                        EachNewPositionCenter[1] + IntRadius*np.sin(EachNewIntAngle))

            fig = plt.figure()
            ax = plt.axes(xlim=(-Radius-1, Radius+1),
                          ylim=(-Radius-1, Radius+1))
            plt.suptitle(
                "Individual linear motion yields to circular movement illusion ("+str(DotNumber)+" points)")

            ListLines = []
            for cont in range(DotNumber):
                AuxLine, = ax.plot([], [], 'ro', lw=2)
                ListLines.append(AuxLine)
            if ShowCircCenter:
                CenterLine, = ax.plot([], [], 'bo', lw=2)
                MiddleDot = []
                for num in range(StepNumb):
                    AuxSum0 = 0
                    AuxSum1 = 0
                    for cont in range(DotNumber):
                        AuxSum0 = AuxSum0+DotsPositionList[cont][0][num]
                        AuxSum1 = AuxSum1+DotsPositionList[cont][1][num]
                    MiddleDot.append([AuxSum0/DotNumber, AuxSum1/DotNumber])
                ListLines.append(CenterLine)
            plt.plot([Radius*np.cos(t) for t in TimeDiscr],
                     [Radius*np.sin(t) for t in TimeDiscr], 'black', lw=2)

            def animate(i):
                for cont in range(DotNumber):
                    ListLines[cont].set_data([DotsPositionList[cont][0][i]], [
                        DotsPositionList[cont][1][i]])
                if ShowCircCenter:
                    CenterLine.set_data([MiddleDot[i][0]], [MiddleDot[i][1]])
                return ListLines

            if ShowTrajectories:
                for cont in range(DotNumber):
                    plt.plot(
                        DotsPositionList[cont][0], DotsPositionList[cont][1], 'black', lw=.5)

            anim = ani.FuncAnimation(fig, animate, init_func=None,
                                     frames=StepNumb, interval=20, blit=True)

            plt.axis('equal')
            plt.show()
        else:
            raise ValueError("Number of dots must be a positive integer.")
    except:
        raise ValueError("Check arguments.")

############################
#          EXAMPLES        #
############################

#HypocycloidCurve(2, 1.5, 3, np.pi, np.pi/2, ShowTrajectories=True)
#HypocycloidIllusion(DotNumber=25, ShowTrajectories=True, ShowCircCenter=True)
