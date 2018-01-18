/**
 * \file boundary.cpp
 * \brief Implementation of boundary::BoundaryBase, type::Boundary, and factory function.
 * \author Anush Krishnan (anus@bu.edu)
 * \author Olivier Mesnard (mesnardo@gwu.edu)
 * \author Pi-Yueh Chuang (pychuang@gwu.edu)
 * \copyright MIT.
 */

# include <petibm/boundary.h>
# include <petibm/boundarysimple.h>


namespace petibm
{
namespace boundary
{


// default destructor
BoundaryBase::~BoundaryBase()
{
    PetscFunctionBeginUser;
    PetscErrorCode ierr;
    PetscBool finalized;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    comm = MPI_COMM_NULL;
}


PetscErrorCode BoundaryBase::destroy()
{
    PetscFunctionBeginUser;

    std::vector<std::vector<type::SingleBoundary>>().swap(bds);

    comm = MPI_COMM_NULL;
    mpiSize = mpiRank = 0;
    mesh.reset();

    PetscFunctionReturn(0);
}

PetscErrorCode createBoundary(
        const type::Mesh &mesh, const YAML::Node &node,
        type::Boundary &boundary)
{
    PetscFunctionBeginUser;
    
    boundary = std::make_shared<BoundarySimple>(mesh, node);
    
    PetscFunctionReturn(0);
}

}
}
